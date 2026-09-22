using System;
using System.Threading;
using System.Threading.Tasks;
using ISAI.Application.Abstractions;
using ISAI.Application.Auth.Dtos;
using ISAI.Domain.Entities;
using ISAI.Domain.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace ISAI.Application.Auth;

public class AuthService : IAuthService
{
    private readonly IIsaiDbContext _dbContext;
    private readonly IPasswordHasher _passwordHasher;
    private readonly IJwtTokenGenerator _jwtTokenGenerator;
    private readonly ICurrentUserService _currentUserService;

    public AuthService(
        IIsaiDbContext dbContext,
        IPasswordHasher passwordHasher,
        IJwtTokenGenerator jwtTokenGenerator,
        ICurrentUserService currentUserService)
    {
        _dbContext = dbContext;
        _passwordHasher = passwordHasher;
        _jwtTokenGenerator = jwtTokenGenerator;
        _currentUserService = currentUserService;
    }

    public async Task<AuthResponseDto> RegisterAsync(RegisterRequestDto request, CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(request.Email) || string.IsNullOrWhiteSpace(request.Password))
        {
            throw new ArgumentException("Email and password are required.");
        }

        var normalizedEmail = request.Email.Trim().ToLowerInvariant();
        var existingUser = await _dbContext.Users.FirstOrDefaultAsync(u => u.Email == normalizedEmail, cancellationToken);
        if (existingUser != null)
        {
            throw new InvalidOperationException("User with this email already exists.");
        }

        var user = new User
        {
            Email = normalizedEmail,
            PasswordHash = _passwordHasher.HashPassword(request.Password),
            DisplayName = string.IsNullOrWhiteSpace(request.DisplayName) ? normalizedEmail.Split('@')[0] : request.DisplayName.Trim()
        };

        _dbContext.Users.Add(user);
        
        var userPref = new UserPreference
        {
            UserId = user.Id
        };
        _dbContext.UserPreferences.Add(userPref);

        var (accessToken, accessExpires) = _jwtTokenGenerator.GenerateAccessToken(user);
        var (refreshToken, refreshExpires) = _jwtTokenGenerator.GenerateRefreshToken();

        var tokenEntity = new RefreshToken
        {
            UserId = user.Id,
            Token = refreshToken,
            ExpiresAt = refreshExpires
        };
        _dbContext.RefreshTokens.Add(tokenEntity);

        await _dbContext.SaveChangesAsync(cancellationToken);

        return new AuthResponseDto(
            accessToken,
            accessExpires,
            refreshToken,
            refreshExpires,
            new UserDto(user.Id, user.Email, user.DisplayName));
    }

    public async Task<AuthResponseDto> LoginAsync(LoginRequestDto request, CancellationToken cancellationToken = default)
    {
        var normalizedEmail = request.Email.Trim().ToLowerInvariant();
        var user = await _dbContext.Users.FirstOrDefaultAsync(u => u.Email == normalizedEmail, cancellationToken);
        if (user == null || !_passwordHasher.VerifyPassword(request.Password, user.PasswordHash))
        {
            throw new UnauthorizedAccessException("Invalid email or password.");
        }

        var (accessToken, accessExpires) = _jwtTokenGenerator.GenerateAccessToken(user);
        var (refreshToken, refreshExpires) = _jwtTokenGenerator.GenerateRefreshToken();

        var tokenEntity = new RefreshToken
        {
            UserId = user.Id,
            Token = refreshToken,
            ExpiresAt = refreshExpires
        };
        _dbContext.RefreshTokens.Add(tokenEntity);

        await _dbContext.SaveChangesAsync(cancellationToken);

        return new AuthResponseDto(
            accessToken,
            accessExpires,
            refreshToken,
            refreshExpires,
            new UserDto(user.Id, user.Email, user.DisplayName));
    }

    public async Task<AuthResponseDto> RefreshTokenAsync(RefreshTokenRequestDto request, CancellationToken cancellationToken = default)
    {
        var tokenEntity = await _dbContext.RefreshTokens
            .Include(rt => rt.User)
            .FirstOrDefaultAsync(rt => rt.Token == request.RefreshToken && !rt.IsRevoked, cancellationToken);

        if (tokenEntity == null || tokenEntity.ExpiresAt <= DateTime.UtcNow || tokenEntity.User == null)
        {
            throw new UnauthorizedAccessException("Invalid or expired refresh token.");
        }

        tokenEntity.IsRevoked = true;

        var user = tokenEntity.User;
        var (newAccessToken, newAccessExpires) = _jwtTokenGenerator.GenerateAccessToken(user);
        var (newRefreshToken, newRefreshExpires) = _jwtTokenGenerator.GenerateRefreshToken();

        var newTokenEntity = new RefreshToken
        {
            UserId = user.Id,
            Token = newRefreshToken,
            ExpiresAt = newRefreshExpires
        };
        _dbContext.RefreshTokens.Add(newTokenEntity);

        await _dbContext.SaveChangesAsync(cancellationToken);

        return new AuthResponseDto(
            newAccessToken,
            newAccessExpires,
            newRefreshToken,
            newRefreshExpires,
            new UserDto(user.Id, user.Email, user.DisplayName));
    }

    public async Task<UserDto?> GetCurrentUserAsync(CancellationToken cancellationToken = default)
    {
        if (!_currentUserService.IsAuthenticated || !_currentUserService.UserId.HasValue)
        {
            return null;
        }

        var user = await _dbContext.Users.FirstOrDefaultAsync(u => u.Id == _currentUserService.UserId.Value, cancellationToken);
        return user == null ? null : new UserDto(user.Id, user.Email, user.DisplayName);
    }
}
