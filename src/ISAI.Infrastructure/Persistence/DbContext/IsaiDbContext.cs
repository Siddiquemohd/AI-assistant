using System;
using ISAI.Application.Abstractions;
using ISAI.Domain.Entities;
using ISAI.Domain.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace ISAI.Infrastructure.Persistence.DbContext;

public class IsaiDbContext : Microsoft.EntityFrameworkCore.DbContext, IIsaiDbContext
{
    private readonly ICurrentUserService _currentUserService;

    public IsaiDbContext(
        DbContextOptions<IsaiDbContext> options,
        ICurrentUserService currentUserService) : base(options)
    {
        _currentUserService = currentUserService;
    }

    public DbSet<User> Users => Set<User>();
    public DbSet<RefreshToken> RefreshTokens => Set<RefreshToken>();
    public DbSet<UserPreference> UserPreferences => Set<UserPreference>();
    public DbSet<Conversation> Conversations => Set<Conversation>();
    public DbSet<Message> Messages => Set<Message>();
    public DbSet<Memory> Memories => Set<Memory>();
    public DbSet<TaskItem> Tasks => Set<TaskItem>();
    public DbSet<Reminder> Reminders => Set<Reminder>();
    public DbSet<AgentRun> AgentRuns => Set<AgentRun>();
    public DbSet<ToolExecution> ToolExecutions => Set<ToolExecution>();
    public DbSet<DataExport> DataExports => Set<DataExport>();
    public DbSet<AuditEvent> AuditEvents => Set<AuditEvent>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<User>()
            .HasIndex(u => u.Email)
            .IsUnique();

        modelBuilder.Entity<RefreshToken>()
            .HasIndex(rt => rt.Token)
            .IsUnique();

        modelBuilder.Entity<RefreshToken>()
            .HasOne(rt => rt.User)
            .WithMany(u => u.RefreshTokens)
            .HasForeignKey(rt => rt.UserId)
            .OnDelete(DeleteBehavior.Cascade);

        modelBuilder.Entity<UserPreference>()
            .HasKey(up => up.UserId);

        modelBuilder.Entity<UserPreference>()
            .HasOne(up => up.User)
            .WithOne()
            .HasForeignKey<UserPreference>(up => up.UserId)
            .OnDelete(DeleteBehavior.Cascade);

        modelBuilder.Entity<Conversation>()
            .HasQueryFilter(c => c.DeletedAt == null && (!_currentUserService.IsAuthenticated || c.UserId == _currentUserService.UserId));

        modelBuilder.Entity<Conversation>()
            .HasOne(c => c.User)
            .WithMany(u => u.Conversations)
            .HasForeignKey(c => c.UserId)
            .OnDelete(DeleteBehavior.Restrict);

        modelBuilder.Entity<Message>()
            .HasOne(m => m.Conversation)
            .WithMany(c => c.Messages)
            .HasForeignKey(m => m.ConversationId)
            .OnDelete(DeleteBehavior.Cascade);

        modelBuilder.Entity<Memory>()
            .HasQueryFilter(m => m.DeletedAt == null && (!_currentUserService.IsAuthenticated || m.UserId == _currentUserService.UserId));

        modelBuilder.Entity<Memory>()
            .HasOne(m => m.User)
            .WithMany(u => u.Memories)
            .HasForeignKey(m => m.UserId)
            .OnDelete(DeleteBehavior.Restrict);

        modelBuilder.Entity<TaskItem>()
            .HasQueryFilter(t => t.DeletedAt == null && (!_currentUserService.IsAuthenticated || t.UserId == _currentUserService.UserId));

        modelBuilder.Entity<TaskItem>()
            .HasOne(t => t.User)
            .WithMany(u => u.Tasks)
            .HasForeignKey(t => t.UserId)
            .OnDelete(DeleteBehavior.Restrict);

        modelBuilder.Entity<Reminder>()
            .HasQueryFilter(r => r.DeletedAt == null && (!_currentUserService.IsAuthenticated || r.UserId == _currentUserService.UserId));

        modelBuilder.Entity<Reminder>()
            .HasIndex(r => r.IdempotencyKey)
            .IsUnique();

        modelBuilder.Entity<Reminder>()
            .HasOne(r => r.User)
            .WithMany(u => u.Reminders)
            .HasForeignKey(r => r.UserId)
            .OnDelete(DeleteBehavior.Restrict);

        modelBuilder.Entity<AgentRun>()
            .HasOne(ar => ar.User)
            .WithMany()
            .HasForeignKey(ar => ar.UserId)
            .OnDelete(DeleteBehavior.Restrict);

        modelBuilder.Entity<ToolExecution>()
            .HasOne(te => te.AgentRun)
            .WithMany(ar => ar.ToolExecutions)
            .HasForeignKey(te => te.AgentRunId)
            .OnDelete(DeleteBehavior.Cascade);

        modelBuilder.Entity<DataExport>()
            .HasOne(de => de.User)
            .WithMany()
            .HasForeignKey(de => de.UserId)
            .OnDelete(DeleteBehavior.Cascade);

        modelBuilder.Entity<AuditEvent>()
            .HasOne<User>()
            .WithMany()
            .HasForeignKey(ae => ae.UserId)
            .OnDelete(DeleteBehavior.SetNull);
    }
}
