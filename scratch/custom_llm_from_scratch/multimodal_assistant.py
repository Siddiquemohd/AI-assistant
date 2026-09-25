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
from web_scraper_engine import WebScraperEngine
from code_debugger_engine import CodeDebuggerEngine
from market_analytics_engine import MarketAnalyticsEngine
from media_transcoder_engine import MediaTranscoderEngine
from interview_coach_engine import InterviewCoachEngine
from live_voice_mode_engine import LiveVoiceModeEngine
from pdf_qa_engine import PDFQAEngine
from project_generator_engine import ProjectGeneratorEngine
from morning_briefing_engine import MorningBriefingEngine
from news_feed_engine import NewsFeedEngine

# New Engines (31-35)
from webhook_automator_engine import WebhookAutomatorEngine
from sql_query_engine import SQLQueryEngine
from voice_translator_engine import VoiceTranslatorEngine
from resume_builder_engine import ResumeBuilderEngine
from fitness_coach_engine import FitnessCoachEngine

class MultimodalPersonalAI:
    """
    Unified Uncensored Multimodal Super-AI Framework (35 Capability Engines).
    Operates 100% unrestricted without content filters across text, voice, vision, code, math, finance, SQL, fitness, and webhooks.
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

        # Engines 26-30
        self.live_voice = LiveVoiceModeEngine()
        self.pdf_qa = PDFQAEngine()
        self.project_gen = ProjectGeneratorEngine()
        self.morning_briefing = MorningBriefingEngine()
        self.news_feed = NewsFeedEngine()

        # Engines 31-35
        self.webhook_automator = WebhookAutomatorEngine()
        self.sql_query = SQLQueryEngine()
        self.voice_translator = VoiceTranslatorEngine()
        self.resume_builder = ResumeBuilderEngine()
        self.fitness_coach = FitnessCoachEngine()

    def process(self, prompt: str, voice_key: str = "aria", image_path: str = None, file_path: str = None) -> dict:
        prompt_clean = prompt.strip().lower()

        # Emotion Analysis
        emotion_res = self.emotion_engine.detect_emotion(prompt)

        # 1. Fitness & Health Coach Intent
        if any(w in prompt_clean for w in ["workout plan", "fitness coach", "meal plan", "macros"]):
            fit_res = self.fitness_coach.generate_workout_plan(prompt)
            routine_str = "\n".join(fit_res["weekly_routine"])
            return {
                "type": "fitness_coach",
                "response": f"🏋️ **Personalized Fitness & Workout Routine**:\n{routine_str}\n\n**Macros**: {fit_res['recommended_macros']}",
                "details": fit_res
            }

        # 2. Cover Letter & Resume Builder Intent
        if any(w in prompt_clean for w in ["cover letter", "resume builder", "job application"]):
            res_res = self.resume_builder.build_cover_letter("Senior AI Engineer", "Tech Corporation")
            return {
                "type": "resume_builder",
                "response": f"📄 **Custom Cover Letter Output**:\n```text\n{res_res['cover_letter']}\n```",
                "details": res_res
            }

        # 3. SQL Query Architect Intent
        if any(w in prompt_clean for w in ["sql query", "write sql", "database query", "postgres sql"]):
            sql_res = self.sql_query.generate_sql(prompt)
            return {
                "type": "sql_query",
                "response": f"🗄️ **Generated Optimized SQL Query**:\n```sql\n{sql_res['generated_sql']}\n```",
                "details": sql_res
            }

        # 4. Webhook Automator Intent
        if any(w in prompt_clean for w in ["trigger webhook", "call api", "automation webhook"]):
            wh_res = self.webhook_automator.trigger_webhook("https://api.isai.automation/webhook")
            return {
                "type": "webhook_automation",
                "response": f"⚡ **Automation Webhook Executed**:\n{wh_res['message']}",
                "details": wh_res
            }

        # 5. Morning Briefing Intent
        if any(w in prompt_clean for w in ["morning briefing", "daily digest", "morning report"]):
            briefing_res = self.morning_briefing.generate_briefing()
            return {
                "type": "morning_briefing",
                "response": f"☀️ **Daily Personal Morning Briefing**:\n{briefing_res['summary_text']}",
                "details": briefing_res
            }

        # 6. Tech News Feed Intent
        if any(w in prompt_clean for w in ["news feed", "tech news", "latest headlines", "rss news"]):
            news_res = self.news_feed.fetch_latest_tech_news()
            articles_str = "\n".join([f"- **{a['title']}** ({a['source']}): {a['summary']}" for a in news_res["articles"]])
            return {
                "type": "news_feed",
                "response": f"📰 **Latest Tech & AI News Digest**:\n{articles_str}",
                "details": news_res
            }

        # 7. Project Generator Intent
        if any(w in prompt_clean for w in ["generate project", "build project", "create app project", "full code base"]):
            proj_res = self.project_gen.generate_project(prompt)
            manifest_str = "\n".join([f"- `{f['path']}`: {f['description']}" for f in proj_res["file_manifest"]])
            return {
                "type": "project_generator",
                "response": f"🚀 **Project Code Generator Output**:\n{proj_res['summary']}\n\n**Generated Manifest**:\n{manifest_str}",
                "details": proj_res
            }

        # 8. System Diagnostics Intent
        if any(w in prompt_clean for w in ["system health", "diagnostics", "latency", "uptime", "engine status"]):
            diag_res = self.diagnostics.get_health_metrics()
            return {
                "type": "diagnostics",
                "response": (
                    f"⚙️ **System Diagnostics & Health Check**:\n"
                    f"- Status: **{diag_res['status']}**\n"
                    f"- Active Engines: **35 Capability Engines Online**\n"
                    f"- Uptime: `{diag_res['uptime_formatted']}`\n"
                    f"- Memory Usage: `{diag_res['memory_usage_mb']} MB`\n"
                    f"- API Latency: `{diag_res['api_latency_ms']} ms`\n"
                    f"- Content Refusal Rate: `{diag_res['uncensored_filter_status']}`"
                ),
                "details": diag_res
            }

        # 9. General Uncensored Chat Response (with Emotion Intelligence)
        uncensored_res = self.uncensored_engine.process_uncensored(prompt)
        return {
            "type": "uncensored_chat",
            "response": (
                f"Hello! I processed your message: **\"{prompt}\"**.\n\n"
                f"I am **ISAI**, your personal AI assistant running 100% uncensored without content filters. "
                f"All 35 capability engines are live on Render 24/7. "
                f"(Detected Sentiment: *{emotion_res['detected_emotion'].title()}* | Recommended Tone: *{emotion_res['recommended_tone']}*)"
            ),
            "details": uncensored_res,
            "emotion_metadata": emotion_res
        }

if __name__ == "__main__":
    ai = MultimodalPersonalAI()
    print("35-Engine ISAI Personal AI Assistant Suite initialized successfully!")
