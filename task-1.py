import kaggle_benchmarks as kbench
import textwrap


@kbench.task(name="MPT-Bench - 2026.3.22 - Part 1")
def solve_math_problems(llm) -> tuple[int, int]:
    prompt = textwrap.dedent(
        r"""
    Please answer the following 10 multiple-choice questions. Show your work and clearly state your final choice (A, B, C, or D) for each question.

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
    )

    response = llm.prompt(prompt)

    criteria = [
        "The final answer for Question 1 is exactly D.",
        "The final answer for Question 2 is exactly D.",
        "The final answer for Question 3 is exactly B.",
        "The final answer for Question 4 is exactly C.",
        "The final answer for Question 5 is exactly D.",
        "The final answer for Question 6 is exactly C.",
        "The final answer for Question 7 is exactly C.",
        "The final answer for Question 8 is exactly A.",
        "The final answer for Question 9 is exactly A.",
        "The final answer for Question 10 is exactly A.",
    ]

    assessment = kbench.assertions.assess_response_with_judge(
        criteria=criteria, response_text=response, judge_llm=kbench.judge_llm
    )

    if assessment is None:
        kbench.assertions.assert_fail(
            expectation="Judge LLM failed to return a valid assessment."
        )
        return 0, 30

    earned_score = 0
    passed_statuses = []

    for result in assessment.results:
        passed_statuses.append(result.passed)
        if result.passed:
            earned_score += 3
        kbench.assertions.assert_true(
            result.passed,
            expectation=f"Criterion failed: '{result.criterion}'. Reason: {result.reason}",
        )

    return earned_score, 30


solve_math_problems.run(kbench.llm)
