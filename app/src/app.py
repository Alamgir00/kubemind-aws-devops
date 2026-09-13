from flask import Flask

app = Flask(__name__)

CALCULATOR_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KubeMind AI Calculator</title>
<style>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', Roboto, Arial, sans-serif;
  }

  body {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    padding: 20px;
  }

  .brand {
    color: #e0f7fa;
    margin-bottom: 18px;
    text-align: center;
  }

  .brand h1 {
    font-size: 22px;
    letter-spacing: 1px;
  }

  .brand span {
    color: #4fd1c5;
  }

  .brand p {
    font-size: 12px;
    color: #90a4ae;
    margin-top: 4px;
  }

  .calculator {
    width: 340px;
    max-width: 92vw;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 20px;
    backdrop-filter: blur(14px);
    box-shadow: 0 20px 45px rgba(0, 0, 0, 0.45);
  }

  .display {
    background: rgba(0, 0, 0, 0.35);
    border-radius: 14px;
    padding: 18px 16px;
    margin-bottom: 16px;
    text-align: right;
    overflow: hidden;
    min-height: 90px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
  }

  #expression {
    color: #90a4ae;
    font-size: 15px;
    min-height: 18px;
    word-break: break-all;
  }

  #result {
    color: #ffffff;
    font-size: 34px;
    font-weight: 600;
    word-break: break-all;
  }

  .buttons {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
  }

  button {
    border: none;
    border-radius: 12px;
    padding: 16px 0;
    font-size: 18px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.08s ease, filter 0.15s ease;
    color: #eceff1;
    background: rgba(255, 255, 255, 0.08);
  }

  button:hover {
    filter: brightness(1.2);
  }

  button:active {
    transform: scale(0.94);
  }

  .op {
    background: linear-gradient(135deg, #4fd1c5, #38b2ac);
    color: #06282a;
  }

  .equal {
    background: linear-gradient(135deg, #ff8a65, #ff7043);
    color: #2b0f08;
    grid-column: span 2;
  }

  .clear, .del {
    background: linear-gradient(135deg, #ef5350, #e53935);
    color: #2b0505;
  }

  .zero {
    grid-column: span 2;
  }

  footer {
    margin-top: 16px;
    color: #607d8b;
    font-size: 12px;
    text-align: center;
  }
</style>
</head>
<body>

  <div class="brand">
    <h1>🚀 Kube<span>Mind</span> AI</h1>
    <p>Smart Calculator · by Sakil</p>
  </div>

  <div class="calculator">
    <div class="display">
      <div id="expression"></div>
      <div id="result">0</div>
    </div>

    <div class="buttons">
      <button class="clear" onclick="clearAll()">AC</button>
      <button class="del" onclick="deleteLast()">⌫</button>
      <button class="op" onclick="appendValue('%')">%</button>
      <button class="op" onclick="appendValue('/')">÷</button>

      <button onclick="appendValue('7')">7</button>
      <button onclick="appendValue('8')">8</button>
      <button onclick="appendValue('9')">9</button>
      <button class="op" onclick="appendValue('*')">×</button>

      <button onclick="appendValue('4')">4</button>
      <button onclick="appendValue('5')">5</button>
      <button onclick="appendValue('6')">6</button>
      <button class="op" onclick="appendValue('-')">−</button>

      <button onclick="appendValue('1')">1</button>
      <button onclick="appendValue('2')">2</button>
      <button onclick="appendValue('3')">3</button>
      <button class="op" onclick="appendValue('+')">+</button>

      <button class="zero" onclick="appendValue('0')">0</button>
      <button onclick="appendValue('.')">.</button>
      <button class="equal" onclick="calculate()">=</button>
    </div>
  </div>

  <footer>KubeMind AI Pipeline Service</footer>

  <script>
    const expressionEl = document.getElementById('expression');
    const resultEl = document.getElementById('result');
    let expression = '';

    function updateDisplay() {
      expressionEl.textContent = expression;
      resultEl.textContent = expression === '' ? '0' : liveEvaluate();
    }

    function liveEvaluate() {
      try {
        const sanitized = expression.replace(/%/g, '/100');
        const value = Function('"use strict"; return (' + sanitized + ')')();
        if (value === undefined || Number.isNaN(value)) return expression;
        return formatNumber(value);
      } catch (e) {
        return expression;
      }
    }

    function formatNumber(num) {
      if (!isFinite(num)) return 'Error';
      return Number(num.toFixed(10)).toString();
    }

    function appendValue(val) {
      const lastChar = expression.slice(-1);
      const operators = ['+', '-', '*', '/', '%'];

      if (operators.includes(val) && operators.includes(lastChar)) {
        expression = expression.slice(0, -1) + val;
      } else {
        expression += val;
      }
      updateDisplay();
    }

    function clearAll() {
      expression = '';
      updateDisplay();
    }

    function deleteLast() {
      expression = expression.slice(0, -1);
      updateDisplay();
    }

    function calculate() {
      if (expression === '') return;
      try {
        const sanitized = expression.replace(/%/g, '/100');
        const value = Function('"use strict"; return (' + sanitized + ')')();
        if (value === undefined || Number.isNaN(value) || !isFinite(value)) {
          resultEl.textContent = 'Error';
          expression = '';
          return;
        }
        resultEl.textContent = formatNumber(value);
        expression = formatNumber(value).toString();
      } catch (e) {
        resultEl.textContent = 'Error';
        expression = '';
      }
    }

    document.addEventListener('keydown', function (e) {
      const key = e.key;
      if (/[0-9]/.test(key)) {
        appendValue(key);
      } else if (['+', '-', '*', '/', '%', '.'].includes(key)) {
        appendValue(key);
      } else if (key === 'Enter' || key === '=') {
        e.preventDefault();
        calculate();
      } else if (key === 'Backspace') {
        deleteLast();
      } else if (key === 'Escape') {
        clearAll();
      }
    });

    updateDisplay();
  </script>

</body>
</html>
"""


@app.route("/")
def home():
    return CALCULATOR_HTML


@app.route("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
