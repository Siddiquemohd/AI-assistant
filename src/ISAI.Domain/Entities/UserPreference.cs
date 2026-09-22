using System;

namespace ISAI.Domain.Entities;

public class UserPreference
{
    public Guid UserId { get; set; }
    public User? User { get; set; }
    public string Theme { get; set; } = "System"; // Light, Dark, System
    public string Timezone { get; set; } = "UTC";
    public bool VoiceEnabled { get; set; } = true;
    public bool ProactiveAssistance { get; set; } = false;
    public string QuietHoursStart { get; set; } = "22:00";
    public string QuietHoursEnd { get; set; } = "07:00";
    public string AssistantPersonality { get; set; } = "Friendly and concise";
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
}
