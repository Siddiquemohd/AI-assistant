using System;
using ISAI.Domain.Entities;

namespace ISAI.Domain.Interfaces;

public interface IJwtTokenGenerator
{
    (string AccessToken, DateTime AccessTokenExpiresAt) GenerateAccessToken(User user);
    (string RefreshToken, DateTime RefreshTokenExpiresAt) GenerateRefreshToken();
}
