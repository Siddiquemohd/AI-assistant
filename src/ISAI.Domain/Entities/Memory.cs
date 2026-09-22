using System;

namespace ISAI.Domain.Entities;

public class Memory
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid UserId { get; set; }
    public User? User { get; set; }
    public string Content { get; set; } = string.Empty;
    public string Category { get; set; } = "General"; // Preference, Fact, Work, Personal
    public string Source { get; set; } = "UserExplicit"; // UserExplicit, SystemSuggested
    public string SensitivityLevel { get; set; } = "Normal"; // Normal, Private, Confidential
    public bool IsEnabled { get; set; } = true;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? DeletedAt { get; set; }
}
