import os
from math_engine import MathEngine
from vision_image_engine import VisionImageEngine
from code_interpreter_engine import CodeInterpreterEngine
from audio_speech_engine import AudioSpeechEngine
from web_search_engine import WebSearchEngine
from document_parser_engine import DocumentParserEngine
from translation_engine import TranslationEngine
from data_visualization_engine import DataVisualizationEngine
from crypto_security_engine import CryptoSecurityEngine
from voice_engine import UltraRealisticVoiceEngine
from uncensored_engine import UncensoredEngine
from uncensored_vision_engine import UncensoredVisionImageEngine
from file_system_engine import FileSystemAutomatorEngine
from knowledge_graph_engine import KnowledgeGraphEngine
from emotion_engine import EmotionIntelligenceEngine
from ocr_vision_engine import OCRVisionEngine
from agent_planner_engine import AgentPlannerEngine
from smart_home_engine import SmartHomeEngine
from system_diagnostics_engine import SystemDiagnosticsEngine

# New Engines (21-25)
from web_scraper_engine import WebScraperEngine
from code_debugger_engine import CodeDebuggerEngine
from market_analytics_engine import MarketAnalyticsEngine
from media_transcoder_engine import MediaTranscoderEngine
from interview_coach_engine import InterviewCoachEngine

class MultimodalPersonalAI:
    """
    Unified Uncensored Multimodal Super-AI Framework (25 Capability Engines).
    Operates 100% unrestricted without content filters across text, voice, vision, code, math, finance, and deep research.
    """

    def __init__(self):
        self.math_engine = MathEngine()
        self.image_engine = VisionImageEngine()
        self.uncensored_vision = UncensoredVisionImageEngine()
        self.code_engine = CodeInterpreterEngine()
        self.audio_engine = AudioSpeechEngine()
        self.web_engine = WebSearchEngine()
        self.doc_engine = DocumentParserEngine()
        self.trans_engine = TranslationEngine()
        self.chart_engine = DataVisualizationEngine()
        self.crypto_engine = CryptoSecurityEngine()
        self.voice_engine = UltraRealisticVoiceEngine()
        self.uncensored_engine = UncensoredEngine()
        self.file_engine = FileSystemAutomatorEngine()
        
        # Engines 15-20
        self.knowledge_graph = KnowledgeGraphEngine()
        self.emotion_engine = EmotionIntelligenceEngine()
        self.ocr_engine = OCRVisionEngine()
        self.agent_planner = AgentPlannerEngine()
        self.smart_home = SmartHomeEngine()
        self.diagnostics = SystemDiagnosticsEngine()

        # Engines 21-25
        self.web_scraper = WebScraperEngine()
        self.code_debugger = CodeDebuggerEngine()
        self.market_analytics = MarketAnalyticsEngine()
        self.media_transcoder = MediaTranscoderEngine()
        self.interview_coach = InterviewCoachEngine()

    def process(self, prompt: str, voice_key: str = "aria", image_path: str = None, file_path: str = None) -> dict:
        prompt_clean = prompt.strip().lower()

        # Emotion Analysis
        emotion_res = self.emotion_engine.detect_emotion(prompt)

        # 1. Financial & Crypto Market Intent
        if any(w in prompt_clean for w in ["market", "stock", "crypto", "btc", "eth", "rsi"]):
            market_res = self.market_analytics.analyze_asset(prompt)
            return {
                "type": "market_analytics",
                "response": f"📈 **Market Analytics Result**:\nAsset: `{market_res['symbol']}` | Trend: **{market_res['trend']}** | Signal: **{market_res['macd_signal']}**\nSummary: {market_res['summary']}",
                "details": market_res
            }

        # 2. Code Debugger Intent
        if any(w in prompt_clean for w in ["debug code", "refactor", "fix bug", "code vulnerability"]):
            debug_res = self.code_debugger.debug_and_refactor(prompt)
            return {
                "type": "code_debugger",
                "response": f"🛠️ **Code Debugger & Refactor Result**:\nBugs Detected: {', '.join(debug_res['bugs_detected'])}\n```python\n{debug_res['refactored_code']}\n```",
                "details": debug_res
            }

        # 3. Prompt Refinement / Interview Intent
        if any(w in prompt_clean for w in ["refine prompt", "optimize prompt", "grill me", "mock interview"]):
            coach_res = self.interview_coach.refine_prompt(prompt)
            return {
                "type": "prompt_refactor",
                "response": f"💡 **Refined Prompt Engineering**:\nScore: `{coach_res['prompt_score']}`\n\n```markdown\n{coach_res['refined_prompt']}\n```",
                "details": coach_res
            }

        # 4. Web Scraper Deep Research Intent
        if any(w in prompt_clean for w in ["scrape url", "deep research", "read url", "extract web"]):
            scrape_res = self.web_scraper.deep_research_url(prompt)
            return {
                "type": "deep_research",
                "response": f"🌐 **Deep Research Extraction**:\nURL: `{scrape_res['url']}`\n" + "\n".join(scrape_res["key_takeaways"]),
                "details": scrape_res
            }

        # 5. Media Transcoder Intent
        if any(w in prompt_clean for w in ["convert audio", "transcode media", "convert video"]):
            media_res = self.media_transcoder.convert_media(prompt)
            return {
                "type": "media_transcoder",
                "response": f"🎵 **Media Transcode Result**:\nOutput File: `{media_res['output_file']}` (Bitrate: {media_res['bitrate']})",
                "details": media_res
            }

        # 6. System Diagnostics Intent
        if any(w in prompt_clean for w in ["system health", "diagnostics", "latency", "uptime", "engine status"]):
            diag_res = self.diagnostics.get_health_metrics()
            return {
                "type": "diagnostics",
                "response": (
                    f"⚙️ **System Diagnostics & Health Check**:\n"
                    f"- Status: **{diag_res['status']}**\n"
                    f"- Active Engines: **25 Capability Engines Online**\n"
                    f"- Uptime: `{diag_res['uptime_formatted']}`\n"
                    f"- Memory Usage: `{diag_res['memory_usage_mb']} MB`\n"
                    f"- API Latency: `{diag_res['api_latency_ms']} ms`\n"
                    f"- Content Refusal Rate: `{diag_res['uncensored_filter_status']}`"
                ),
                "details": diag_res
            }

        # 7. Autonomous Agentic Task Planner Intent
        if any(w in prompt_clean for w in ["plan goal", "autonomous task", "breakdown goal", "agent plan"]):
            plan_res = self.agent_planner.plan_and_execute_goal(prompt)
            steps_str = "\n".join(plan_res["plan_breakdown"])
            return {
                "type": "agent_plan",
                "response": f"🎯 **Autonomous Agent Goal Execution**:\n{steps_str}\n\n**Summary**: {plan_res['summary_report']}",
                "details": plan_res
            }

        # 8. OCR Visual Text Extraction Intent
        if any(w in prompt_clean for w in ["ocr", "extract text from image", "read document scan"]):
            ocr_res = self.ocr_engine.extract_text_from_image(image_path or "sample.png")
            return {
                "type": "ocr_extraction",
                "response": f"📷 **OCR Text Extraction Result**:\n```text\n{ocr_res['extracted_text']}\n```",
                "details": ocr_res
            }

        # 9. Smart Home Automation Intent
        if any(w in prompt_clean for w in ["turn on light", "turn off light", "ac temperature", "thermostat"]):
            home_res = self.smart_home.execute_command(prompt)
            return {
                "type": "smart_home",
                "response": f"🏠 **Smart Home Automation Executed**:\nAction: {home_res.get('action', home_res.get('message'))}",
                "details": home_res
            }

        # 10. Personal Knowledge Graph Intent
        if any(w in prompt_clean for w in ["remember triple", "save relationship", "knowledge graph"]):
            kg_res = self.knowledge_graph.add_relation("User", "prefers", prompt)
            return {
                "type": "knowledge_graph",
                "response": f"🧠 **Knowledge Graph Triple Saved**:\nSaved relationship: `User -> prefers -> {prompt}`",
                "details": kg_res
            }

        # 11. Uncensored Image Generation Intent
        if any(w in prompt_clean for w in ["generate image", "create image", "draw", "make image", "uncensored art"]):
            out_file = "generated_image_uncensored.png"
            img_res = self.uncensored_vision.generate_image_uncensored(prompt, output_path=out_file)
            return {
                "type": "uncensored_image_generation",
                "response": f"[Uncensored Vision Engine]: Image generated without content filters!\nSaved to: `{img_res['file_path']}`",
                "details": img_res
            }

        # 12. Uncensored Image Editing Intent
        if any(w in prompt_clean for w in ["edit image", "blur image", "grayscale", "brighten"]):
            target_img = image_path or "generated_image_uncensored.png"
            action = "grayscale"
            if "blur" in prompt_clean:
                action = "blur"
            elif "brighten" in prompt_clean:
                action = "brightness"

            out_file = f"edited_image_uncensored_{action}.png"
            edit_res = self.uncensored_vision.edit_image_uncensored(target_img, action=action, output_path=out_file)
            return {
                "type": "uncensored_image_editing",
                "response": f"[Uncensored Vision Engine]: Image edit ({action}) completed without content filters!\nSaved to: `{edit_res.get('output_file')}`",
                "details": edit_res
            }

        # 13. File System Automator Intent
        if any(w in prompt_clean for w in ["inspect folder", "list directory", "inspect files", "list files"]):
            fs_res = self.file_engine.inspect_directory(".")
            return {
                "type": "file_system",
                "response": f"[File System Automator]: Inspected directory `{fs_res['directory']}`\nFound {fs_res['file_count']} files and {fs_res['subdir_count']} subdirectories.",
                "details": fs_res
            }

        # 14. Ultra-Realistic Female Voice Synthesis (10 Neural Voices)
        if any(w in prompt_clean for w in ["speak", "say in voice", "female voice", "read out"]):
            voice_res = self.voice_engine.speak(
                text=prompt.replace("speak", "").replace("say in voice", "").strip() or prompt,
                voice_key=voice_key,
                output_path="output_speech.mp3"
            )
            return {
                "type": "voice_synthesis",
                "response": f"[Ultra-Realistic Female Voice]: Generated voice audio using '{voice_res['voice_name']}'.\nSaved to: `{voice_res['file_path']}`",
                "details": voice_res
            }

        # 15. Multilingual Translation Intent
        if any(w in prompt_clean for w in ["translate", "spanish", "french", "german", "hindi"]):
            target = "es"
            if "french" in prompt_clean:
                target = "fr"
            elif "german" in prompt_clean:
                target = "de"
            elif "hindi" in prompt_clean:
                target = "hi"
            res = self.trans_engine.translate(prompt.replace("translate", "").strip(), target_lang=target)
            return {
                "type": "translation",
                "response": f"[Translation Engine ({res['target_language'].upper()})]:\nOriginal: {res['original_text']}\nTranslated: **{res['translated_text']}**",
                "details": res
            }

        # 16. Data Visualization Intent
        if any(w in prompt_clean for w in ["chart", "plot graph", "bar chart"]):
            res = self.chart_engine.generate_bar_chart(
                labels=["Q1", "Q2", "Q3", "Q4"],
                values=[45.0, 78.0, 62.0, 95.0],
                title="Performance Overview",
                output_path="output_chart.png"
            )
            return {
                "type": "visualization",
                "response": f"[Data Visualization Engine]: Plotted chart successfully!\nSaved to: `{res['file_path']}`",
                "details": res
            }

        # 17. Crypto Security & Hashing Intent
        if any(w in prompt_clean for w in ["hash", "sha256", "encode base64", "password security"]):
            if "password" in prompt_clean:
                res = self.crypto_engine.evaluate_password_security(prompt)
                return {
                    "type": "security_eval",
                    "response": f"[Security Engine]: Password Strength: **{res['strength']}** (Score: {res['score']}/100)",
                    "details": res
                }
            else:
                res = self.crypto_engine.hash_text(prompt)
                return {
                    "type": "crypto_hash",
                    "response": f"[Security Engine (SHA256)]:\nHash: `{res['hash_value']}`",
                    "details": res
                }

        # 18. Code Execution Intent
        if any(w in prompt_clean for w in ["execute code", "run python", "run code", "def ", "import "]):
            code_result = self.code_engine.execute_python(prompt)
            return {
                "type": "code_execution",
                "response": f"[Code Interpreter Output]:\n```text\n{code_result.get('output', code_result.get('error'))}\n```",
                "details": code_result
            }

        # 19. Math Solving Intent
        if any(w in prompt_clean for w in ["solve", "derivative", "integral", "equation", "+", "-", "*", "/", "calculus"]):
            math_result = self.math_engine.solve(prompt)
            if math_result.get("status") == "Success":
                return {
                    "type": "math",
                    "response": f"[Math Engine Solution]:\n{math_result['latex']}\n\n*Result*: `{math_result.get('result', math_result.get('solutions'))}`",
                    "details": math_result
                }

        # 20. General Uncensored Chat Response (with Emotion Intelligence)
        uncensored_res = self.uncensored_engine.process_uncensored(prompt)
        return {
            "type": "uncensored_chat",
            "response": (
                f"Hello! I processed your message: **\"{prompt}\"**.\n\n"
                f"I am **ISAI**, your personal AI assistant running 100% uncensored without content filters. "
                f"All 25 capability engines are live on Render 24/7. "
                f"(Detected Sentiment: *{emotion_res['detected_emotion'].title()}* | Recommended Tone: *{emotion_res['recommended_tone']}*)"
            ),
            "details": uncensored_res,
            "emotion_metadata": emotion_res
        }

if __name__ == "__main__":
    ai = MultimodalPersonalAI()
    print("25-Engine ISAI Personal AI Assistant initialized successfully!")
