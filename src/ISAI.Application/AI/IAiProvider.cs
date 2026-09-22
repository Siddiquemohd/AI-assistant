using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace ISAI.Application.AI;

public record AiMessagePrompt(string Role, string Content);

public interface IAiProvider
{
    Task<string> GenerateResponseAsync(IEnumerable<AiMessagePrompt> history, CancellationToken cancellationToken = default);
    IAsyncEnumerable<string> StreamResponseAsync(IEnumerable<AiMessagePrompt> history, CancellationToken cancellationToken = default);
}
