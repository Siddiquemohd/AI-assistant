using System;
using System.Collections.Generic;

namespace ISAI.Domain.Entities;

public class Conversation
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid UserId { get; set; }
    public User? User { get; set; }
    public string Title { get; set; } = "New Conversation";
    public string Status { get; set; } = "Active"; // Active, Archived, Deleted
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? DeletedAt { get; set; }

    public ICollection<Message> Messages { get; set; } = new List<Message>();
}
