import re
import sympy as sp

class MathEngine:
    """
    Mathematical Reasoning & Problem Solving Engine.
    Executes algebra, calculus, arithmetic, and symbolic math with step-by-step LaTeX rendering.
    """

    def solve(self, query: str) -> dict:
        query_clean = query.strip()

        try:
            # 1. Calculus: Derivative
            if "derivative" in query_clean.lower() or "diff" in query_clean.lower():
                match = re.search(r'(?:derivative|diff)\s+(?:of\s+)?(.+?)(?:\s+wrt|\s+with respect to|\s+x)?$', query_clean, re.IGNORECASE)
                expr_str = match.group(1).strip() if match else "x**2"
                x = sp.Symbol('x')
                expr = sp.sympify(expr_str)
                result = sp.diff(expr, x)
                return {
                    "status": "Success",
                    "type": "Calculus Derivative",
                    "expression": str(expr),
                    "result": str(result),
                    "latex": f"\\[ \\frac{{d}}{{dx}} \\left( {sp.latex(expr)} \\right) = {sp.latex(result)} \\]"
                }

            # 2. Calculus: Integral
            if "integral" in query_clean.lower() or "integrate" in query_clean.lower():
                match = re.search(r'(?:integral|integrate)\s+(?:of\s+)?(.+)', query_clean, re.IGNORECASE)
                expr_str = match.group(1).strip() if match else "x**2"
                x = sp.Symbol('x')
                expr = sp.sympify(expr_str)
                result = sp.integrate(expr, x)
                return {
                    "status": "Success",
                    "type": "Calculus Integral",
                    "expression": str(expr),
                    "result": f"{result} + C",
                    "latex": f"\\[ \\int \\left( {sp.latex(expr)} \\right) dx = {sp.latex(result)} + C \\]"
                }

            # 3. Algebra Equation Solving
            if "=" in query_clean or "solve" in query_clean.lower():
                eq_str = query_clean.lower().replace("solve", "").strip()
                x = sp.Symbol('x')
                if "=" in eq_str:
                    lhs, rhs = eq_str.split("=")
                    equation = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
                else:
                    equation = sp.Eq(sp.sympify(eq_str), 0)

                solutions = sp.solve(equation, x)
                return {
                    "status": "Success",
                    "type": "Algebraic Equation",
                    "equation": str(equation),
                    "solutions": [str(s) for s in solutions],
                    "latex": f"\\[ x = {', '.join([sp.latex(s) for s in solutions])} \\]"
                }

            # 4. General Numerical & Symbolic Arithmetic
            expr = sp.sympify(query_clean)
            evaluated = expr.evalf()
            return {
                "status": "Success",
                "type": "Arithmetic / Symbolic Evaluation",
                "expression": str(expr),
                "result": str(evaluated),
                "latex": f"\\[ {sp.latex(expr)} = {sp.latex(evaluated)} \\]"
            }

        except Exception as e:
            return {
                "status": "Error",
                "query": query,
                "error": str(e)
            }
