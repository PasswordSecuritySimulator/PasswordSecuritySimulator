import ast
import re

def analyze_code(code):
    findings = []

    try:
        tree = ast.parse(code)

        dangerous_functions = {
            "eval": "استخدام eval قد يسمح بتنفيذ مدخلات غير موثوقة.",
            "exec": "استخدام exec قد يسمح بتنفيذ كود ديناميكي.",
            "system": "استخدام system لتنفيذ أوامر النظام.",
            "popen": "استخدام popen لتشغيل أوامر النظام.",
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):

                if isinstance(node.func, ast.Name):
                    function_name = node.func.id

                    if function_name in dangerous_functions:
                        findings.append(
                            f"⚠️ {function_name}: "
                            f"{dangerous_functions[function_name]}"
                        )

                elif isinstance(node.func, ast.Attribute):
                    function_name = node.func.attr

                    if function_name in dangerous_functions:
                        findings.append(
                            f"⚠️ {function_name}: "
                            f"{dangerous_functions[function_name]}"
                        )

    except SyntaxError:
        findings.append("⚠️ يوجد خطأ في بناء جملة الكود.")

    suspicious_patterns = {
        r"requests\.get": "اتصال HTTP قد يستخدم لجلب بيانات.",
        r"urllib": "استخدام مكتبات الاتصال بالإنترنت.",
        r"subprocess": "استخدام subprocess لتشغيل عمليات خارجية.",
        r"socket": "استخدام اتصالات الشبكة.",
        r"base64": "استخدام Base64 قد يرتبط بإخفاء البيانات.",
    }

    for pattern, message in suspicious_patterns.items():
        if re.search(pattern, code, re.IGNORECASE):
            findings.append(f"🔎 {message}")

    findings = list(dict.fromkeys(findings))

    if not findings:
        return "✅ لم يتم العثور على مؤشرات مشبوهة واضحة."

    result = "⚠️ نتائج التحليل:\n\n"
    result += "\n".join(findings)
    result += "\n\n🛡️ التوصية: راجع الكود قبل تشغيله."

    return result

# اختبار المحلل
test_code = """
import subprocess
eval(user_input)
"""

print(analyze_code(test_code))