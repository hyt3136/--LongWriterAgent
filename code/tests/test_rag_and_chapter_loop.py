import unittest

from wenben_engine.graph.chapter_loop import run_chapter_loop
from wenben_engine.rag.context_builder import assemble_context
from wenben_engine.rag.retrieval import fetch_recent_chapters, search_vector_context


class RagAndChapterLoopTestCase(unittest.TestCase):
    def test_rag_retrieval_and_context(self):
        corpus = [
            {"text": "主角在都市觉醒", "source": "c1"},
            {"text": "宗门大战爆发", "source": "c2"},
            {"text": "都市线推进", "source": "c3"},
        ]
        retrieved = search_vector_context("都市 主角", corpus, top_k=2)
        recent = fetch_recent_chapters([
            {"summary": "上一章主角入城"},
            {"summary": "上一章遭遇追杀"},
        ])
        context = assemble_context(retrieved, recent, max_chars=200)

        self.assertGreaterEqual(len(context["chunks"]), 1)
        self.assertLessEqual(context["used_chars"], 200)

    def test_chapter_loop(self):
        context = {"chunks": [{"text": "关键线索A"}, {"text": "关键线索B"}]}
        result = run_chapter_loop("第一章", context, max_rounds=2)

        self.assertIn(result["status"], {"passed", "early_stop", "max_rounds"})
        self.assertIn("draft", result)
        self.assertIn("review", result)


if __name__ == "__main__":
    unittest.main()
