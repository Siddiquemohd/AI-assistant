using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;

namespace ISAI.Application.AI;

public class MockAiProvider : IAiProvider
{
    public Task<string> GenerateResponseAsync(IEnumerable<AiMessagePrompt> history, CancellationToken cancellationToken = default)
    {
        var lastUserMsg = history.LastOrDefault(m => m.Role == "user")?.Content ?? "Hello";
        var response = $"Hello! I am ISAI, your personal AI assistant. You said: '{lastUserMsg}'. How can I assist you today?";
        return Task.FromResult(response);
    }

    public async IAsyncEnumerable<string> StreamResponseAsync(
        IEnumerable<AiMessagePrompt> history,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        var fullResponse = await GenerateResponseAsync(history, cancellationToken);
        var words = fullResponse.Split(' ');
        foreach (var word in words)
        {
            if (cancellationToken.IsCancellationRequested) yield break;
            yield return word + " ";
            await Task.Delay(50, cancellationToken);
        }
    }
}
