using System;
using System.Threading.Tasks;
using ISAI.Application.Auth;
using ISAI.Application.Auth.Dtos;
using ISAI.Domain.Entities;
using ISAI.Domain.Interfaces;
using ISAI.Infrastructure.Auth;
using ISAI.Infrastructure.Persistence.DbContext;
using ISAI.Infrastructure.Services;
using Microsoft.AspNetCore.Http;
using Microsoft.EntityFrameworkCore;
using Xunit;

namespace ISAI.UnitTests;

public class AuthServiceTests
{
    private IsaiDbContext GetDbContext()
    {
        var options = new DbContextOptionsBuilder<IsaiDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;

        var httpContextAccessor = new HttpContextAccessor();
        var currentUserService = new CurrentUserService(httpContextAccessor);
        return new IsaiDbContext(options, currentUserService);
    }

    [Fact]
    public async Task RegisterAsync_ValidRequest_CreatesUserAndReturnsTokens()
    {
        // Arrange
        var dbContext = GetDbContext();
        var passwordHasher = new PasswordHasher();
        var configuration = new Microsoft.Extensions.Configuration.ConfigurationBuilder().Build();
        var jwtGenerator = new JwtTokenGenerator(configuration);
        var httpContextAccessor = new HttpContextAccessor();
        var currentUserService = new CurrentUserService(httpContextAccessor);

        var authService = new AuthService(dbContext, passwordHasher, jwtGenerator, currentUserService);
        var request = new RegisterRequestDto("testuser@example.com", "Password123!", "Test User");

        // Act
        var result = await authService.RegisterAsync(request);

        // Assert
        Assert.NotNull(result);
        Assert.False(string.IsNullOrWhiteSpace(result.AccessToken));
        Assert.False(string.IsNullOrWhiteSpace(result.RefreshToken));
        Assert.Equal("testuser@example.com", result.User.Email);
        Assert.Equal("Test User", result.User.DisplayName);

        var userInDb = await dbContext.Users.FirstOrDefaultAsync(u => u.Email == "testuser@example.com");
        Assert.NotNull(userInDb);
        Assert.True(passwordHasher.VerifyPassword("Password123!", userInDb.PasswordHash));
    }

    [Fact]
    public async Task LoginAsync_ValidCredentials_ReturnsTokens()
    {
        // Arrange
        var dbContext = GetDbContext();
        var passwordHasher = new PasswordHasher();
        var configuration = new Microsoft.Extensions.Configuration.ConfigurationBuilder().Build();
        var jwtGenerator = new JwtTokenGenerator(configuration);
        var httpContextAccessor = new HttpContextAccessor();
        var currentUserService = new CurrentUserService(httpContextAccessor);

        var authService = new AuthService(dbContext, passwordHasher, jwtGenerator, currentUserService);
        var regRequest = new RegisterRequestDto("login@example.com", "SecretPass123!", "Login User");
        await authService.RegisterAsync(regRequest);

        // Act
        var loginRequest = new LoginRequestDto("login@example.com", "SecretPass123!");
        var result = await authService.LoginAsync(loginRequest);

        // Assert
        Assert.NotNull(result);
        Assert.False(string.IsNullOrWhiteSpace(result.AccessToken));
        Assert.Equal("login@example.com", result.User.Email);
    }

    [Fact]
    public async Task LoginAsync_InvalidPassword_ThrowsUnauthorizedAccessException()
    {
        // Arrange
        var dbContext = GetDbContext();
        var passwordHasher = new PasswordHasher();
        var configuration = new Microsoft.Extensions.Configuration.ConfigurationBuilder().Build();
        var jwtGenerator = new JwtTokenGenerator(configuration);
        var httpContextAccessor = new HttpContextAccessor();
        var currentUserService = new CurrentUserService(httpContextAccessor);

        var authService = new AuthService(dbContext, passwordHasher, jwtGenerator, currentUserService);
        var regRequest = new RegisterRequestDto("user2@example.com", "SecretPass123!", "User Two");
        await authService.RegisterAsync(regRequest);

        // Act & Assert
        var loginRequest = new LoginRequestDto("user2@example.com", "WrongPassword");
        await Assert.ThrowsAsync<UnauthorizedAccessException>(() => authService.LoginAsync(loginRequest));
    }
}
