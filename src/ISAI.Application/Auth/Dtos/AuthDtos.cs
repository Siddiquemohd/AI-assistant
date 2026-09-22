using System;

namespace ISAI.Application.Auth.Dtos;

public record RegisterRequestDto(string Email, string Password, string DisplayName);
public record LoginRequestDto(string Email, string Password);
public record RefreshTokenRequestDto(string AccessToken, string RefreshToken);
public record AuthResponseDto(string AccessToken, DateTime AccessTokenExpiresAt, string RefreshToken, DateTime RefreshTokenExpiresAt, UserDto User);
public record UserDto(Guid Id, string Email, string DisplayName);
