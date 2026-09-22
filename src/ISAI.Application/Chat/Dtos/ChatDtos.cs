using System;

namespace ISAI.Application.Chat.Dtos;

public record ConversationDto(Guid Id, string Title, string Status, DateTime CreatedAt, DateTime UpdatedAt);
public record MessageDto(Guid Id, Guid ConversationId, string Role, string Content, string MessageType, string Status, DateTime CreatedAt);
public record CreateConversationRequestDto(string Title);
public record SendMessageRequestDto(string Content);
public record SseEventDto(string EventType, object Data);
