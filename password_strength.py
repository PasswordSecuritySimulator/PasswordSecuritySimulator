import re


def evaluate_password(password: str) -> tuple[int, str, list[str]]:
    """تقييم قوة كلمة المرور وإرجاع الدرجة والوصف وأسباب التحسين."""
    if not isinstance(password, str):
        raise TypeError("يجب أن تكون كلمة المرور نصاً من نوع str.")

    score = 0
    reasons = []

    # 1. التحقق من الطول
    length = len(password)
    if length >= 12:
        score += 35
    elif length >= 8:
        score += 20
        reasons.append("⚠️ يفضل أن تكون كلمة المرور 12 حرفاً أو أكثر لزيادة الأمان.")
    else:
        reasons.append("❌ كلمة المرور قصيرة جداً؛ يجب ألا تقل عن 8 أحرف.")

    # 2. التحقق من وجود حرف كبير وحرف صغير
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 25
    else:
        reasons.append("❌ يجب أن تحتوي كلمة المرور على حروف كبيرة وصغيرة.")

    # 3. التحقق من وجود رقم
    if re.search(r"\d", password):
        score += 20
    else:
        reasons.append("❌ يجب أن تحتوي كلمة المرور على رقم واحد على الأقل.")

    # 4. التحقق من وجود رمز خاص
    if re.search(r"[^A-Za-z0-9\s]", password):
        score += 20
    else:
        reasons.append("❌ يجب أن تحتوي كلمة المرور على رمز خاص، مثل: @ أو # أو $.")

    # تحديد التقييم النهائي من 100
    if score >= 80:
        strength = "قوية جداً 🛡️"
    elif score >= 50:
        strength = "متوسطة ⚠️"
    else:
        strength = "ضعيفة ❌"

    return score, strength, reasons


if __name__ == "__main__":
    # تجربة الدالة
    password = "MySecurePass123!"
    score, strength, reasons = evaluate_password(password)

    print(f"الدرجة: {score}/100")
    print(f"التقييم: {strength}")

    if reasons:
        print("\nملاحظات التحسين:")
        for reason in reasons:
            print(f"- {reason}")
    else:
        print("✅ كلمة المرور تستوفي جميع الشروط.")
