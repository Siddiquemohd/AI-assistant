using System;
using System.Collections.Generic;

namespace ISAI.Domain.Entities;

public class AgentRun
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid UserId { get; set; }
    public User? User { get; set; }
    public Guid? ConversationId { get; set; }
    public string Intent { get; set; } = string.Empty;
    public string Status { get; set; } = "Requested"; // Requested, Analyzing, Planning, AwaitingConfirmation, Authorized, Executing, Completed, Failed, Cancelled
    public string RiskLevel { get; set; } = "Low"; // Low, Medium, High, Critical
    public bool RequiresConfirmation { get; set; }
    public string ConfirmationTokenDigest { get; set; } = string.Empty;
    public DateTime StartedAt { get; set; } = DateTime.UtcNow;
    public DateTime? CompletedAt { get; set; }

    public ICollection<ToolExecution> ToolExecutions { get; set; } = new List<ToolExecution>();
}
