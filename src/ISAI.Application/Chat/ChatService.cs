using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using ISAI.Application.Abstractions;
using ISAI.Application.AI;
using ISAI.Application.Chat.Dtos;
using ISAI.Domain.Entities;
using ISAI.Domain.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace ISAI.Application.Chat;

public class ChatService : IChatService
{
    private readonly IIsaiDbContext _dbContext;
    private readonly ICurrentUserService _currentUserService;
    private readonly IAiProvider _aiProvider;

    public ChatService(IIsaiDbContext dbContext, ICurrentUserService currentUserService, IAiProvider aiProvider)
    {
        _dbContext = dbContext;
        _currentUserService = currentUserService;
        _aiProvider = aiProvider;
    }

    public async Task<IEnumerable<ConversationDto>> GetConversationsAsync(CancellationToken cancellationToken = default)
    {
        if (!_currentUserService.UserId.HasValue)
        {
            throw new UnauthorizedAccessException("User is not authenticated.");
        }

        var conversations = await _dbContext.Conversations
            .Where(c => c.UserId == _currentUserService.UserId.Value)
            .OrderByDescending(c => c.UpdatedAt)
            .ToListAsync(cancellationToken);

        return conversations.Select(c => new ConversationDto(c.Id, c.Title, c.Status, c.CreatedAt, c.UpdatedAt));
    }

    public async Task<ConversationDto> CreateConversationAsync(CreateConversationRequestDto request, CancellationToken cancellationToken = default)
    {
        if (!_currentUserService.UserId.HasValue)
        {
            throw new UnauthorizedAccessException("User is not authenticated.");
        }

        var title = string.IsNullOrWhiteSpace(request.Title) ? "New Conversation" : request.Title.Trim();

        var conversation = new Conversation
        {
            UserId = _currentUserService.UserId.Value,
            Title = title,
            Status = "Active"
        };

        _dbContext.Conversations.Add(conversation);
        await _dbContext.SaveChangesAsync(cancellationToken);

        return new ConversationDto(conversation.Id, conversation.Title, conversation.Status, conversation.CreatedAt, conversation.UpdatedAt);
    }

    public async Task<IEnumerable<MessageDto>> GetMessagesAsync(Guid conversationId, int page = 1, int pageSize = 50, CancellationToken cancellationToken = default)
    {
        if (!_currentUserService.UserId.HasValue)
        {
            throw new UnauthorizedAccessException("User is not authenticated.");
        }

        var conversation = await _dbContext.Conversations
            .FirstOrDefaultAsync(c => c.Id == conversationId && c.UserId == _currentUserService.UserId.Value, cancellationToken);

        if (conversation == null)
        {
            throw new KeyNotFoundException("Conversation not found.");
        }

        var skip = (page - 1) * pageSize;

        var messages = await _dbContext.Messages
            .Where(m => m.ConversationId == conversationId)
            .OrderBy(m => m.CreatedAt)
            .Skip(skip)
            .Take(pageSize)
            .ToListAsync(cancellationToken);

        return messages.Select(m => new MessageDto(m.Id, m.ConversationId, m.Role, m.Content, m.MessageType, m.Status, m.CreatedAt));
    }

    public async Task<MessageDto> SendMessageAsync(Guid conversationId, SendMessageRequestDto request, CancellationToken cancellationToken = default)
    {
        if (!_currentUserService.UserId.HasValue)
        {
            throw new UnauthorizedAccessException("User is not authenticated.");
        }

        if (string.IsNullOrWhiteSpace(request.Content))
        {
            throw new ArgumentException("Message content cannot be empty.");
        }

        var conversation = await _dbContext.Conversations
            .FirstOrDefaultAsync(c => c.Id == conversationId && c.UserId == _currentUserService.UserId.Value, cancellationToken);

        if (conversation == null)
        {
            throw new KeyNotFoundException("Conversation not found.");
        }

        var userMsg = new Message
        {
            ConversationId = conversationId,
            UserId = _currentUserService.UserId.Value,
            Role = "user",
            Content = request.Content.Trim(),
            MessageType = "Text",
            Status = "Completed"
        };
        _dbContext.Messages.Add(userMsg);

        if (conversation.Title == "New Conversation")
        {
            conversation.Title = request.Content.Trim().Length > 30 
                ? request.Content.Trim().Substring(0, 30) + "..." 
                : request.Content.Trim();
        }
        conversation.UpdatedAt = DateTime.UtcNow;

        await _dbContext.SaveChangesAsync(cancellationToken);

        var existingMessages = await _dbContext.Messages
            .Where(m => m.ConversationId == conversationId)
            .OrderBy(m => m.CreatedAt)
            .ToListAsync(cancellationToken);

        var promptHistory = existingMessages.Select(m => new AiMessagePrompt(m.Role, m.Content));

        var aiResponseText = await _aiProvider.GenerateResponseAsync(promptHistory, cancellationToken);

        var assistantMsg = new Message
        {
            ConversationId = conversationId,
            UserId = _currentUserService.UserId.Value,
            Role = "assistant",
            Content = aiResponseText,
            MessageType = "Text",
            Status = "Completed",
            ModelName = "ISAI-MockProvider"
        };
        _dbContext.Messages.Add(assistantMsg);
        await _dbContext.SaveChangesAsync(cancellationToken);

        return new MessageDto(assistantMsg.Id, assistantMsg.ConversationId, assistantMsg.Role, assistantMsg.Content, assistantMsg.MessageType, assistantMsg.Status, assistantMsg.CreatedAt);
    }

    public async IAsyncEnumerable<SseEventDto> StreamMessageAsync(
        Guid conversationId,
        SendMessageRequestDto request,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        if (!_currentUserService.UserId.HasValue)
        {
            throw new UnauthorizedAccessException("User is not authenticated.");
        }

        if (string.IsNullOrWhiteSpace(request.Content))
        {
            throw new ArgumentException("Message content cannot be empty.");
        }

        var conversation = await _dbContext.Conversations
            .FirstOrDefaultAsync(c => c.Id == conversationId && c.UserId == _currentUserService.UserId.Value, cancellationToken);

        if (conversation == null)
        {
            throw new KeyNotFoundException("Conversation not found.");
        }

        // 1. Save user message
        var userMsg = new Message
        {
            ConversationId = conversationId,
            UserId = _currentUserService.UserId.Value,
            Role = "user",
            Content = request.Content.Trim(),
            MessageType = "Text",
            Status = "Completed"
        };
        _dbContext.Messages.Add(userMsg);

        if (conversation.Title == "New Conversation")
        {
            conversation.Title = request.Content.Trim().Length > 30 
                ? request.Content.Trim().Substring(0, 30) + "..." 
                : request.Content.Trim();
        }
        conversation.UpdatedAt = DateTime.UtcNow;

        await _dbContext.SaveChangesAsync(cancellationToken);

        // 2. Prepare assistant placeholder message
        var assistantMsg = new Message
        {
            ConversationId = conversationId,
            UserId = _currentUserService.UserId.Value,
            Role = "assistant",
            Content = "",
            MessageType = "Text",
            Status = "Processing",
            ModelName = "ISAI-MockProvider"
        };
        _dbContext.Messages.Add(assistantMsg);
        await _dbContext.SaveChangesAsync(cancellationToken);

        // Event 1: message.started
        yield return new SseEventDto("message.started", new
        {
            messageId = assistantMsg.Id,
            conversationId = conversationId,
            role = "assistant",
            createdAt = assistantMsg.CreatedAt
        });

        var history = await _dbContext.Messages
            .Where(m => m.ConversationId == conversationId && m.Id != assistantMsg.Id)
            .OrderBy(m => m.CreatedAt)
            .Select(m => new AiMessagePrompt(m.Role, m.Content))
            .ToListAsync(cancellationToken);

        var fullContentBuilder = new StringBuilder();
        var deltaIndex = 0;

        await foreach (var chunk in _aiProvider.StreamResponseAsync(history, cancellationToken))
        {
            if (cancellationToken.IsCancellationRequested)
            {
                assistantMsg.Status = "Interrupted";
                assistantMsg.Content = fullContentBuilder.ToString();
                await _dbContext.SaveChangesAsync(CancellationToken.None);

                yield return new SseEventDto("message.cancelled", new
                {
                    messageId = assistantMsg.Id,
                    cancelledAt = DateTime.UtcNow
                });
                yield break;
            }

            fullContentBuilder.Append(chunk);

            yield return new SseEventDto("message.delta", new
            {
                messageId = assistantMsg.Id,
                chunk = chunk,
                deltaIndex = deltaIndex++
            });
        }

        assistantMsg.Content = fullContentBuilder.ToString();
        assistantMsg.Status = "Completed";
        await _dbContext.SaveChangesAsync(cancellationToken);

        // Event: message.completed
        yield return new SseEventDto("message.completed", new
        {
            messageId = assistantMsg.Id,
            fullContent = assistantMsg.Content,
            tokenUsage = new { promptTokens = 10, completionTokens = 20 },
            status = "Completed",
            persistedAt = DateTime.UtcNow
        });
    }

    public async Task<MessageDto> RetryMessageAsync(Guid conversationId, Guid messageId, CancellationToken cancellationToken = default)
    {
        if (!_currentUserService.UserId.HasValue)
        {
            throw new UnauthorizedAccessException("User is not authenticated.");
        }

        var messageToRetry = await _dbContext.Messages
            .FirstOrDefaultAsync(m => m.Id == messageId && m.ConversationId == conversationId && m.UserId == _currentUserService.UserId.Value, cancellationToken);

        if (messageToRetry == null)
        {
            throw new KeyNotFoundException("Message not found.");
        }

        var sendRequest = new SendMessageRequestDto(messageToRetry.Content);
        return await SendMessageAsync(conversationId, sendRequest, cancellationToken);
    }
}
