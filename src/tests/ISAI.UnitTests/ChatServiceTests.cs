using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using ISAI.Application.AI;
using ISAI.Application.Chat;
using ISAI.Application.Chat.Dtos;
using ISAI.Domain.Entities;
using ISAI.Infrastructure.Persistence.DbContext;
using ISAI.Infrastructure.Services;
using Microsoft.AspNetCore.Http;
using Microsoft.EntityFrameworkCore;
using Xunit;

namespace ISAI.UnitTests;

public class ChatServiceTests
{
    private (IsaiDbContext dbContext, Guid userId) GetDbContextWithUser()
    {
        var options = new DbContextOptionsBuilder<IsaiDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;

        var userId = Guid.NewGuid();
        var httpContext = new DefaultHttpContext();
        httpContext.User = new System.Security.Claims.ClaimsPrincipal(
            new System.Security.Claims.ClaimsIdentity(new[]
            {
                new System.Security.Claims.Claim(System.Security.Claims.ClaimTypes.NameIdentifier, userId.ToString()),
                new System.Security.Claims.Claim(System.Security.Claims.ClaimTypes.Email, "testuser@example.com")
            }, "TestAuth"));

        var httpContextAccessor = new HttpContextAccessor { HttpContext = httpContext };
        var currentUserService = new CurrentUserService(httpContextAccessor);

        var dbContext = new IsaiDbContext(options, currentUserService);
        return (dbContext, userId);
    }

    [Fact]
    public async Task CreateConversation_ValidRequest_CreatesConversationInDb()
    {
        // Arrange
        var (dbContext, userId) = GetDbContextWithUser();
        var currentUserService = new CurrentUserService(new HttpContextAccessor
        {
            HttpContext = new DefaultHttpContext
            {
                User = new System.Security.Claims.ClaimsPrincipal(
                    new System.Security.Claims.ClaimsIdentity(new[]
                    {
                        new System.Security.Claims.Claim(System.Security.Claims.ClaimTypes.NameIdentifier, userId.ToString())
                    }, "TestAuth"))
            }
        });
        var aiProvider = new MockAiProvider();
        var chatService = new ChatService(dbContext, currentUserService, aiProvider);

        // Act
        var result = await chatService.CreateConversationAsync(new CreateConversationRequestDto("My Test Chat"));

        // Assert
        Assert.NotNull(result);
        Assert.Equal("My Test Chat", result.Title);

        var conversations = await chatService.GetConversationsAsync();
        Assert.Single(conversations);
    }

    [Fact]
    public async Task SendMessage_ValidContent_ReturnsAssistantMessageAndPersists()
    {
        // Arrange
        var (dbContext, userId) = GetDbContextWithUser();
        var currentUserService = new CurrentUserService(new HttpContextAccessor
        {
            HttpContext = new DefaultHttpContext
            {
                User = new System.Security.Claims.ClaimsPrincipal(
                    new System.Security.Claims.ClaimsIdentity(new[]
                    {
                        new System.Security.Claims.Claim(System.Security.Claims.ClaimTypes.NameIdentifier, userId.ToString())
                    }, "TestAuth"))
            }
        });
        var aiProvider = new MockAiProvider();
        var chatService = new ChatService(dbContext, currentUserService, aiProvider);

        var conv = await chatService.CreateConversationAsync(new CreateConversationRequestDto("Chat 1"));

        // Act
        var result = await chatService.SendMessageAsync(conv.Id, new SendMessageRequestDto("Hello ISAI!"));

        // Assert
        Assert.NotNull(result);
        Assert.Equal("assistant", result.Role);
        Assert.Contains("Hello ISAI!", result.Content);

        var messages = await chatService.GetMessagesAsync(conv.Id);
        Assert.Equal(2, messages.Count()); // 1 user + 1 assistant
    }

    [Fact]
    public async Task StreamMessage_ValidContent_EmitsStartedDeltaAndCompletedEvents()
    {
        // Arrange
        var (dbContext, userId) = GetDbContextWithUser();
        var currentUserService = new CurrentUserService(new HttpContextAccessor
        {
            HttpContext = new DefaultHttpContext
            {
                User = new System.Security.Claims.ClaimsPrincipal(
                    new System.Security.Claims.ClaimsIdentity(new[]
                    {
                        new System.Security.Claims.Claim(System.Security.Claims.ClaimTypes.NameIdentifier, userId.ToString())
                    }, "TestAuth"))
            }
        });
        var aiProvider = new MockAiProvider();
        var chatService = new ChatService(dbContext, currentUserService, aiProvider);

        var conv = await chatService.CreateConversationAsync(new CreateConversationRequestDto("Streaming Chat"));

        // Act
        var events = new List<SseEventDto>();
        await foreach (var sseEvent in chatService.StreamMessageAsync(conv.Id, new SendMessageRequestDto("Tell me a story")))
        {
            events.Add(sseEvent);
        }

        // Assert
        Assert.True(events.Count > 2);
        Assert.Equal("message.started", events.First().EventType);
        Assert.Equal("message.completed", events.Last().EventType);
    }
}
