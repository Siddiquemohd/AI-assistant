using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using ISAI.Application.Chat.Dtos;

namespace ISAI.Application.Chat;

public interface IChatService
{
    Task<IEnumerable<ConversationDto>> GetConversationsAsync(CancellationToken cancellationToken = default);
    Task<ConversationDto> CreateConversationAsync(CreateConversationRequestDto request, CancellationToken cancellationToken = default);
    Task<IEnumerable<MessageDto>> GetMessagesAsync(Guid conversationId, int page = 1, int pageSize = 50, CancellationToken cancellationToken = default);
    Task<MessageDto> SendMessageAsync(Guid conversationId, SendMessageRequestDto request, CancellationToken cancellationToken = default);
    IAsyncEnumerable<SseEventDto> StreamMessageAsync(Guid conversationId, SendMessageRequestDto request, CancellationToken cancellationToken = default);
    Task<MessageDto> RetryMessageAsync(Guid conversationId, Guid messageId, CancellationToken cancellationToken = default);
}
