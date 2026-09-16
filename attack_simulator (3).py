import time

def password_cracker_simulator():
    # 1. إنشاء قائمة كلمات مرور تجريبية
    password_list = [
        "123456",
        "password",
        "12345678",
        "qwerty",
        "admin",
        "welcome",
        "Cyber123"
    ]

    target_password = "Cyber123"

    print("🧪 محاكاة تعليمية لتخمين كلمات المرور")
    print(f"كلمة المرور المستهدفة: {target_password}")

    # 2. محاكاة التخمين وحساب عدد المحاولات
    attempts_count = 0
    start_time = time.time()
    found = False

    for idx, pwd in enumerate(password_list, 1):
        attempts_count += 1

        print(f"[{idx}] جرب كلمة المرور: {pwd}")
        time.sleep(0.1)

        if pwd == target_password:
            found = True
            break

    end_time = time.time()
    elapsed_time = end_time - start_time

    # 3. عرض نتيجة المحاكاة
    print("\n" + "=" * 40)

    if found:
        print(f"✅ كلمة المرور المكتشفة: {target_password}")
        print(f"🔢 عدد المحاولات: {attempts_count}")
        print(f"⏱️ الزمن المستغرق: {elapsed_time:.2f} ثانية")

        if elapsed_time > 0:
            print(
                f"📊 معدل المحاولات: "
                f"{attempts_count / elapsed_time:.2f} محاولة/ثانية"
            )
    else:
        print("❌ فشل في العثور على كلمة المرور.")
        print(f"🔢 إجمالي عدد المحاولات: {attempts_count}")

    print("=" * 40)


if __name__ == "__main__":
    password_cracker_simulator()