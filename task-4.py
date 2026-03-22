import kaggle_benchmarks as kbench
import textwrap
from pydantic import BaseModel, Field


class Scoring(BaseModel):
    q18_score: int = Field(description="Score for Q18 (0-15).")


@kbench.task(name="MPT-Bench - 2026.3.22 - Part 4")
def gaokao_math_problems(llm) -> tuple[int, int]:
    problem_text = textwrap.dedent(
        r"""
Please solve the following math problem. Show your work and provide a clear final answer for each part.

18. Let \{a_{n}\} and \{b_{n}\} be two arithmetic sequences. Define
c_{n}=\max\{\,b_{1}-a_{1}n,\; b_{2}-a_{2}n,\; \ldots,\; b_{n}-a_{n}n\,\}\quad(n=1,2,3,\ldots),
where \max\{x_{1},x_{2},\ldots,x_{s}\} denotes the largest of these s numbers.
(1) If a_{n}=n,\; b_{n}=2n-1, find the values of c_{1},c_{2},c_{3}, and prove that \{c_{n}\} is an arithmetic sequence.
(2) Prove that either for every positive integer M there exists a positive integer m such that for all n\ge m one has \frac{c_{n}}{n}>M; or there exists a positive integer m such that c_{m},c_{m+1},c_{m+2},\ldots is an arithmetic sequence.
    """
    )

    response = llm.prompt(problem_text)

    judge_prompt = textwrap.dedent(
        f"""
    Evaluate the following student response for the math problem.
    
    Q18 is worth 15 points.
    For this problem, the final answer must be correct, but since it is a proof/derivation:
    - If the answer is perfectly correct and well derived, give full 15 points.
    - Students can use different valid methods. 
    - If there are errors or the proof is interrupted, read their work and give partial credit based on the percentage of completion up to the FIRST logical error or interruption. 
    - Output the integer score for the question.

    Student Response:
    {response}
    """
    )

    try:
        scoring = kbench.judge_llm.prompt(judge_prompt, schema=Scoring)
        earned_score = scoring.q18_score

        q18_passed = scoring.q18_score >= (15 * 0.6)
        passed_statuses = [q18_passed]

        kbench.assertions.assert_true(
            scoring.q18_score == 15, expectation=f"Q18 Score: {scoring.q18_score}/15"
        )

        return earned_score, 15
    except Exception as e:
        kbench.assertions.assert_fail(expectation=f"Judging failed: {str(e)}")
        return 0, 15


gaokao_math_problems.run(kbench.llm)
