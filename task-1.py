import kaggle_benchmarks as kbench
from kaggle_benchmarks.prompting import ResponseParsingError
from pydantic import BaseModel, Field
from typing import List


class MultipleChoiceAnswers(BaseModel):
    answers: List[str] = Field(
        description="A list of the chosen options (e.g., ['A', 'B', 'C', ...]) for the 10 questions.",
        min_length=10,
        max_length=10,
    )


@kbench.task(name="MPT-Bench - 2026.3.22 - Part 1")
def solve_math_problems(llm) -> tuple[int, int, list[bool]]:
    prompt = r"""
Please answer the following 10 multiple-choice questions. Your response must be a JSON object with a single key ‘answers’ which holds a list of 10 strings, where each string is the letter of the correct option (A, B, C, or D).

1. The directrix of the parabola \(x^{2}=4y\) is (  )
A. \(x=1\)  B. \(x=-1\)  C. \(y=1\)  D. \(y=-1\)

2. Let \(f(x)\) be an even function with domain \(\mathbb{R}\), monotone increasing on \((0,+\infty)\), and satisfying \(f(x_{1}x_{2})=f(x_{1})f(x_{2})\) for any \(x_{1},x_{2}\). Which of the following functions meets the conditions?
A. \(y=\ln|x|\)  B. \(y=x^{3}\)  C. \(y=2^{|x|}\)  D. \(y=|x|\)

3. The maximum value of the distance from the point \((0,-1)\) to the line \(y=k(x+1)\) is (  )
A. \(1\)  B. \(\sqrt{2}\)  C. \(\sqrt{3}\)  D. \(2\)

4. Given \(f(x)=e^{x}-e^{4-x}\), then (  )
A. The graph of \(f(x)\) is symmetric about the line \(x=-2\)
B. The graph of \(f(x)\) is symmetric about the point \((-2,0)\)
C. The graph of \(f(x)\) is symmetric about the point \((2,0)\)
D. The graph of \(f(x)\) is symmetric about the line \(x=2\)

5. Let ellipse \(C:\frac{x^2}{a^2}+\frac{y^2}{3}=1\ (a>0)\) have left and right foci \(F_{1},F_{2}\). A line \(l\) through \(F_{2}\) with nonzero slope meets \(C\) at \(A,B\). If the perimeter of \(\triangle ABF_{1}\) is \(8\), then the eccentricity of \(C\) is (  )
A. \(\frac{\sqrt{3}}{4}\)  B. \(\frac{1}{4}\)  C. \(\frac{\sqrt{3}}{2}\)  D. \(\frac{1}{2}\)

6. Let \(S_{n}\) be the sum of the first \(n\) terms of sequence \(\{a_{n}\}\), with \(q\neq 0,\ a_{1}\neq 0\). The statement “\((1-q)S_{n}=a_{1}(1-q^{n})\)” is the (  ) of “the sequence \(\{a_{n}\}\) is a geometric sequence with common ratio \(q\)”.
A. necessary and sufficient condition
B. sufficient but not necessary condition
C. necessary but not sufficient condition
D. neither sufficient nor necessary condition

7. A right circular cylinder is inscribed in a sphere of radius \(1\). When the volume of the cylinder is maximal, its height is (  )
A. \(\frac{1}{2}\)  B. \(\frac{\sqrt{3}}{3}\)  C. \(\frac{2\sqrt{3}}{3}\)  D. \(\frac{\sqrt{2}}{2}\)

8. Given the circles \(C_{1}:x^{2}+y^{2}=1\) and \(C_{2}:(x-3)^{2}+y^{2}=r^{2}\) \((r>0)\). There are three common tangents to \(C_{1}\) and \(C_{2}\). A circle \(C\) covers (contains) both \(C_{1}\) and \(C_{2}\). The minimum area of circle \(C\) is \(\underline{\hspace{4cm}}\).
A. \(9\pi\)  B. \(12\pi\)  C. \(16\pi\)  D. \(18\pi\)

9. In the cube \(ABCD\text{-}A_{1}B_{1}C_{1}D_{1}\) with edge length \(2\), let \(M\) be the midpoint of \(A_{1}D_{1}\). Let \(N\) be a moving point on the lateral face \(B_{1}CC_{1}B_{1}\), and suppose \(MN\parallel\) plane \(A_{1}BD\). The maximum possible length of segment \(MN\) is \(\underline{\hspace{4cm}}\).
A. \(2\sqrt{2}\)  B. \(\sqrt{2}\)  C. \(\sqrt{5}\)  D. \(\sqrt{6}\)

10. Let point \(M(x_{0},1)\). If there exists a point \(N\) on the circle \(O: x^{2}+y^{2}=1\) such that \(\angle OMN=45^{\circ}\), then the range of \(x_{0}\) is \(\underline{\hspace{4cm}}\).
A. \([-1,1]\)  B. \(\left[-\frac{1}{2},\frac{1}{2}\right]\)  C. \([-\sqrt{2},\sqrt{2}]\)  D. \(\left[-\frac{\sqrt{2}}{2},\frac{\sqrt{2}}{2}\right]\)
    """
    correct_answers = ["D", "D", "B", "C", "D", "C", "C", "A", "A", "A"]
    total_score = len(correct_answers) * 3
    earned_score = 0
    passed_statuses = []

    try:
        response = llm.prompt(prompt, schema=MultipleChoiceAnswers)

        model_answers = [ans.strip().upper() for ans in response.answers]

        for i, (model_ans, correct_ans) in enumerate(
            zip(model_answers, correct_answers)
        ):
            is_correct = model_ans == correct_ans
            passed_statuses.append(is_correct)
            if is_correct:
                earned_score += 3
            kbench.assertions.assert_true(
                is_correct,
                expectation=f"Question {i+1}: Expected '{correct_ans}', but got '{model_ans}'.",
            )

    except ResponseParsingError as e:
        kbench.assertions.assert_fail(
            expectation=f"The output was not valid JSON or did not match the schema. Error: {e.error}"
        )
        return 0, total_score, [False] * 10

    return earned_score, total_score, passed_statuses


solve_math_problems.run(kbench.llm)
