using System;

namespace ISAI.Domain.Entities;

public class ToolExecution
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid AgentRunId { get; set; }
    public AgentRun? AgentRun { get; set; }
    public string ToolName { get; set; } = string.Empty;
    public string ToolVersion { get; set; } = "1.0";
    public string InputMetadataJson { get; set; } = "{}";
    public string Status { get; set; } = "Executing"; // Executing, Completed, Failed, Cancelled
    public string ResultMetadataJson { get; set; } = "{}";
    public int ExecutionTimeMs { get; set; }
    public DateTime StartedAt { get; set; } = DateTime.UtcNow;
    public DateTime? CompletedAt { get; set; }
}
