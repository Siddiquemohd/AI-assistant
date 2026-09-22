using System;

namespace ISAI.Domain.Entities;

public class Message
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid ConversationId { get; set; }
    public Conversation? Conversation { get; set; }
    public Guid UserId { get; set; }
    public string Role { get; set; } = string.Empty; // user, assistant, system, tool
    public string Content { get; set; } = string.Empty;
    public string MessageType { get; set; } = "Text"; // Text, Code, Voice, ToolResult
    public string Status { get; set; } = "Completed"; // Sending, Processing, Completed, Interrupted, Failed
    public int PromptTokens { get; set; }
    public int CompletionTokens { get; set; }
    public string ModelName { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
