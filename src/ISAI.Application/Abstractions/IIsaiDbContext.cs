using System.Threading;
using System.Threading.Tasks;
using ISAI.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace ISAI.Application.Abstractions;

public interface IIsaiDbContext
{
    DbSet<User> Users { get; }
    DbSet<RefreshToken> RefreshTokens { get; }
    DbSet<UserPreference> UserPreferences { get; }
    DbSet<Conversation> Conversations { get; }
    DbSet<Message> Messages { get; }
    DbSet<Memory> Memories { get; }
    DbSet<TaskItem> Tasks { get; }
    DbSet<Reminder> Reminders { get; }
    DbSet<AgentRun> AgentRuns { get; }
    DbSet<ToolExecution> ToolExecutions { get; }
    DbSet<DataExport> DataExports { get; }
    DbSet<AuditEvent> AuditEvents { get; }

    Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
}
