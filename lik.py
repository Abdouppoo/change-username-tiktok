import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# الدالة لإرسال اللايكات
def send_likes(uid):
    url = f'https://mahmoud-aheqh0b3csgagdf4.eastus-01.azurewebsites.net/likes?uid={uid}&key=c4-kj00llkaj'
    try:
        response = requests.get(url)

        # التحقق من حالة الاستجابة
        if response.status_code == 200:
            try:
                data = response.json()  # محاولة قراءة JSON
                if 'status' in data and data['status'] == 'success':
                    result = f"✅ تم إرسال اللايكات بنجاح للمعرف: {uid}"
                elif 'status' in data and data['status'] == 'error':
                    result = f"❌ خطأ: {data.get('message', 'حدث خطأ غير متوقع.')}"
                else:
                    result = "❌ استجابة غير متوقعة من الخادم."
            except ValueError:
                # عرض النص الخام للاستجابة
                result = f"By ABDOU:\n{response.text}"
        else:
            # عرض النص الخام للاستجابة مع حالة الخطأ
            result = f"❌ خطأ: حالة الخادم {response.status_code}.\nالرد: {response.text}"
    except requests.RequestException as e:
        result = f"❌ حدث خطأ أثناء الاتصال بالخادم: {str(e)}"

    # حذف النصوص غير المرغوب فيها
    unwanted_texts = [
        "By C4 Team Officiel",
        "Tg ChAnnel > @C4_Team_Officiel",
        "Tg Chat > @C4_Team_Chat",
        "Officiel Website > https://c4teampro.free.bg"
    ]

    for text in unwanted_texts:
        result = result.replace(text, "")

    return result

# الدالة التي تتعامل مع أمر /abdou
async def handle_send_likes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        uid = context.args[0]
        if not uid.isdigit():
            await update.message.reply_text("❌ يرجى إدخال UID صالح (أرقام فقط).")
            return
        result = send_likes(uid)
        await update.message.reply_text(result)
    else:
        await update.message.reply_text("يرجى إدخال UID بعد الأمر.\nمثال: /abdou 123456789")

# إعداد البوت وتشغيله
def main():
    # طلب إدخال التوكن من المستخدم
    token = "8050394387:AAEQgwFkMf1pe-UeJsn9W5XxYKP-VvXXa94"  # ضع التوكن الخاص بالبوت هنا

    # إعداد تطبيق البوت
    application = Application.builder().token(token).build()

    # تعيين الأمر /abdou للتعامل مع وظيفة handle_send_likes
    application.add_handler(CommandHandler("like", handle_send_likes))

    # بدء تشغيل البوت
    application.run_polling()

if __name__ == '__main__':
    main()