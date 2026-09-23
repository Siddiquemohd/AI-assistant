import io
import sys
import traceback

class CodeInterpreterEngine:
    """
    Code Execution & Sandbox Interpreter Engine.
    Executes Python code snippets dynamically, evaluates mathematical algorithms, and captures stdout output.
    """

    def execute_python(self, code: str) -> dict:
        code_clean = code.strip()

        # Remove markdown code block ticks if present
        if code_clean.startswith("```python"):
            code_clean = code_clean[9:]
        if code_clean.startswith("```"):
            code_clean = code_clean[3:]
        if code_clean.endswith("```"):
            code_clean = code_clean[:-3]

        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output

        global_vars = {"__builtins__": __builtins__}
        local_vars = {}

        try:
            exec(code_clean.strip(), global_vars, local_vars)
            sys.stdout = old_stdout
            output_str = redirected_output.getvalue()

            # Include return values if defined
            result_summary = local_vars.get("result", output_str.strip())
            return {
                "status": "Success",
                "output": output_str.strip() or str(result_summary),
                "variables": {k: str(v) for k, v in local_vars.items() if not k.startswith("__")}
            }

        except Exception as e:
            sys.stdout = old_stdout
            error_trace = traceback.format_exc()
            return {
                "status": "Error",
                "error": str(e),
                "traceback": error_trace
            }
