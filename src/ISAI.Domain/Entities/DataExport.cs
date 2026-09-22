using System;

namespace ISAI.Domain.Entities;

public class DataExport
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid UserId { get; set; }
    public User? User { get; set; }
    public string RequestType { get; set; } = "FullUserExport";
    public string Status { get; set; } = "Requested"; // Requested, Processing, Completed, Failed
    public string DownloadUrlReference { get; set; } = string.Empty;
    public DateTime RequestedAt { get; set; } = DateTime.UtcNow;
    public DateTime? CompletedAt { get; set; }
}
