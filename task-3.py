import kaggle_benchmarks as kbench
import textwrap
from pydantic import BaseModel, Field


class Scoring(BaseModel):
    q16_score: int = Field(description="Score for Q16 (0-10).")
    q17_score: int = Field(description="Score for Q17 (0-15).")


@kbench.task(name="MPT-Bench - 2026.3.22 - Part 3")
def solve_math_problems(llm) -> tuple[int, int]:
    prompt = textwrap.dedent(
        r"""
Please solve the following two math problems. Show your work and provide a clear final answer for each.

16. Let the function f(x)=4\cos x\cdot\cos\!(x-\frac{2\pi}{3})+1.
(1) Find the intervals on which f(x) is monotonically decreasing;
(2) Find the range of f(x) on the interval [-\frac{\pi}{3},\frac{\pi}{4}].

17. Given the ellipse C:\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1 (a>b>0) whose eccentricity is \frac{1}{2}. The right focus is F, point A(a,0), and |AF|=1.
(1) Find the equation of the ellipse C.
(2) A line l through F (not coincident with the x-axis) meets the ellipse C at points M,N. The lines MA and NA meet the line x=4 at points P and Q, respectively. Find the measure of \angle PFQ.
    """
    )

    response = llm.prompt(prompt)

    judge_prompt = textwrap.dedent(
        f"""
    Evaluate the following student response for two math problems.
    
    Q16 is worth 10 points. Q17 is worth 15 points.
    For these problems, the final answer must be correct, but since they include proofs/derivations:
    - If the answer is perfectly correct and well derived, give full points.
    - Students can use different valid methods. 
    - If there are errors or the proof is interrupted, read their work and give partial credit based on the percentage of completion up to the FIRST logical error or interruption. 
    - Output the integer score for each question.

    Student Response:
    {response}
    """
    )

    try:
        scoring = kbench.judge_llm.prompt(judge_prompt, schema=Scoring)
        earned_score = scoring.q16_score + scoring.q17_score

        kbench.assertions.assert_true(
            scoring.q16_score == 10, expectation=f"Q16 Score: {scoring.q16_score}/10"
        )
        kbench.assertions.assert_true(
            scoring.q17_score == 15, expectation=f"Q17 Score: {scoring.q17_score}/15"
        )

        return earned_score, 25
    except Exception as e:
        kbench.assertions.assert_fail(expectation=f"Judging failed: {str(e)}")
        return 0, 25


solve_math_problems.run(kbench.llm)
