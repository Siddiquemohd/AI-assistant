using System;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using ISAI.Application.Chat;
using ISAI.Application.Chat.Dtos;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace ISAI.Api.Controllers;

[Authorize]
[ApiController]
[Route("api/v1/conversations")]
public class ConversationsController : ControllerBase
{
    private readonly IChatService _chatService;

    public ConversationsController(IChatService chatService)
    {
        _chatService = chatService;
    }

    [HttpGet]
    public async Task<IActionResult> GetConversations(CancellationToken cancellationToken)
    {
        var conversations = await _chatService.GetConversationsAsync(cancellationToken);
        return Ok(conversations);
    }

    [HttpPost]
    public async Task<IActionResult> CreateConversation([FromBody] CreateConversationRequestDto request, CancellationToken cancellationToken)
    {
        var conversation = await _chatService.CreateConversationAsync(request, cancellationToken);
        return CreatedAtAction(nameof(GetMessages), new { conversationId = conversation.Id }, conversation);
    }

    [HttpGet("{conversationId:guid}/messages")]
    public async Task<IActionResult> GetMessages(
        Guid conversationId,
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 50,
        CancellationToken cancellationToken = default)
    {
        try
        {
            var messages = await _chatService.GetMessagesAsync(conversationId, page, pageSize, cancellationToken);
            return Ok(messages);
        }
        catch (KeyNotFoundException ex)
        {
            return NotFound(new { message = ex.Message });
        }
    }

    [HttpPost("{conversationId:guid}/messages")]
    public async Task<IActionResult> SendMessage(Guid conversationId, [FromBody] SendMessageRequestDto request, CancellationToken cancellationToken)
    {
        try
        {
            var message = await _chatService.SendMessageAsync(conversationId, request, cancellationToken);
            return Ok(message);
        }
        catch (KeyNotFoundException ex)
        {
            return NotFound(new { message = ex.Message });
        }
        catch (ArgumentException ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }

    [HttpPost("{conversationId:guid}/messages/stream")]
    public async Task StreamMessage(Guid conversationId, [FromBody] SendMessageRequestDto request, CancellationToken cancellationToken)
    {
        Response.Headers.Append("Content-Type", "text/event-stream");
        Response.Headers.Append("Cache-Control", "no-cache");
        Response.Headers.Append("Connection", "keep-alive");

        try
        {
            await foreach (var sseEvent in _chatService.StreamMessageAsync(conversationId, request, cancellationToken))
            {
                var json = JsonSerializer.Serialize(sseEvent.Data);
                await Response.WriteAsync($"event: {sseEvent.EventType}\ndata: {json}\n\n", cancellationToken);
                await Response.Body.FlushAsync(cancellationToken);
            }
        }
        catch (OperationCanceledException)
        {
            // Client disconnected or stream was cancelled
        }
    }

    [HttpPost("{conversationId:guid}/messages/{messageId:guid}/retry")]
    public async Task<IActionResult> RetryMessage(Guid conversationId, Guid messageId, CancellationToken cancellationToken)
    {
        try
        {
            var message = await _chatService.RetryMessageAsync(conversationId, messageId, cancellationToken);
            return Ok(message);
        }
        catch (KeyNotFoundException ex)
        {
            return NotFound(new { message = ex.Message });
        }
    }
}
