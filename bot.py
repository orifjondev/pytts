from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import edge_tts
import asyncio
import os

TOKEN = "8538815916:AAG5dC-NR4kymHD7dzwe8ccfRf8IVwZiuh0"

# Ovozlar lug'ati (ovoz_id: (voice_code, til_nomi, bayroq))
VOICES = {
    'btn1': ('en-US-AnaNeural', 'Ana (Ingliz)', '🇺🇸'),
    'btn2': ('en-US-GuyNeural', 'Guy (Ingliz)', '🇺🇸'),  
    'btn3': ('ru-RU-DariyaNeural', 'Dariya (Rus)', '🇷🇺'),
    'btn4': ('es-ES-ElviraNeural', 'Elvira (Ispan)', '🇪🇸'),
    'btn5': ('fr-FR-DeniseNeural', 'Denise (Fransuz)', '🇫🇷'),
    'btn6': ('de-DE-KatjaNeural', 'Katja (Nemis)', '🇩🇪'),
    'btn7': ('ja-JP-NanamiNeural', 'Nanami (Yapon)', '🇯🇵'),
    'btn8': ('ko-KR-SunHiNeural', 'Sun-Hi (Koreys)', '🇰🇷'),
    'btn9': ('tr-TR-EmelNeural', 'Emel (Turk)', '🇹🇷'),
    'btn10': ('uz-UZ-MadinaNeural', 'Madina (Oʻzbek)', '🇺🇿'),
    'btn11': ('uz-UZ-SardorNeural', 'Sardor (Oʻzbek)', '🇺🇿')
}

# Har bir til uchun test matnlari (terminalda ko'rinishi uchun)
def print_text_samples():
    print("=" * 70)
    print("🎙️ HAR BIR TIL UCHUN TEST MATNLARI")
    print("=" * 70)
    
    samples = {
        'english': [
            "Hello! Welcome to our Text-to-Speech bot.",
            "The quick brown fox jumps over the lazy dog."
        ],
        'russian': [
            "Привет! Добро пожаловать в наш бот Text-to-Speech.",
            "Съешь ещё этих мягких французских булок, да выпей чаю."
        ],
        'spanish': [
            "¡Hola! Bienvenido a nuestro bot de Text-to-Speech.",
            "El veloz murciélago hindú comía feliz cardillo y kiwi."
        ],
        'french': [
            "Bonjour! Bienvenue dans notre bot Text-to-Speech.",
            "Portez ce vieux whisky au juge blond qui fume."
        ],
        'german': [
            "Hallo! Willkommen bei unserem Text-to-Speech-Bot.",
            "Zwölf Boxkämpfer jagen Viktor quer über den großen Sylter Deich."
        ],
        'japanese': [
            "こんにちは！ Text-to-Speech ボットへようこそ。",
            "色は匂へど散りぬるを我が世誰ぞ常ならむ有為の奥山今日越えて浅き夢見じ酔ひもせず。"
        ],
        'korean': [
            "안녕하세요! Text-to-Speech 봇에 오신 것을 환영합니다.",
            "키스의 고유조건은 입술끼리 만나야 하고 특별한 기술은 필요치 않다."
        ],
        'turkish': [
            "Merhaba! Text-to-Speech botumuza hoş geldiniz.",
            "Pijamalı hasta yağız şoföre çabucak güvendi."
        ],
        'uzbek': [
            "Salom! Text-to-Speech botimizga xush kelibsiz.",
            "Juda qiziq, tez va faol boʻlgan tulki haqida hikoya.",
            "Oʻzbekiston — buyuk kelajakka ega davlat.",
            "Texnologiya hayotimizni har kuni osonlashtiradi."
        ]
    }
    
    for language, texts in samples.items():
        print(f"\n{'='*50}")
        print(f"🌍 TIL: {language.upper()}")
        print(f"{'='*50}")
        for text in texts:
            print(f"• {text}")
    
    print("\n" + "=" * 70)
    print("🎙️ O'ZBEK TILI UCHUN OVOZLAR:")
    print("• uz-UZ-MadinaNeural - Oʻzbek ayol ovoz")
    print("• uz-UZ-SardorNeural - Oʻzbek erkak ovoz")
    print("=" * 70)

# Foydalanuvchi sozlamalari
user_settings = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asosiy menyu"""
    keyboard = [
        # 1-qator
        [
            InlineKeyboardButton("🇺🇸 Ana", callback_data='btn1'),
            InlineKeyboardButton("🇺🇸 Guy", callback_data='btn2'),
            InlineKeyboardButton("🇷🇺 Dariya", callback_data='btn3')
        ],
        # 2-qator
        [
            InlineKeyboardButton("🇪🇸 Elvira", callback_data='btn4'),
            InlineKeyboardButton("🇫🇷 Denise", callback_data='btn5'),
            InlineKeyboardButton("🇩🇪 Katja", callback_data='btn6')
        ],
        # 3-qator
        [
            InlineKeyboardButton("🇯🇵 Nanami", callback_data='btn7'),
            InlineKeyboardButton("🇰🇷 Sun-Hi", callback_data='btn8'),
            InlineKeyboardButton("🇹🇷 Emel", callback_data='btn9')
        ],
        # 4-qator - O'zbek ovozlari
        [
            InlineKeyboardButton("🇺🇿 Madina", callback_data='btn10'),
            InlineKeyboardButton("🇺🇿 Sardor", callback_data='btn11'),
            InlineKeyboardButton("⚙️ Sozlamalar", callback_data='settings')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎙️ **Text-to-Speech Bot (O'zbek tili qo'shildi!)**\n\n"
        "O'zbek tilidagi 2 ta yangi ovoz:\n"
        "• 🇺🇿 Madina - O'zbek ayol ovoz\n"
        "• 🇺🇿 Sardor - O'zbek erkak ovoz\n\n"
        "Ovoz tanlang:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tugmalar bosilganda"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == 'settings':
        # Sozlamalar menyusi
        keyboard = [
            [InlineKeyboardButton("⏩ Tezlik", callback_data='speed_menu')],
            [InlineKeyboardButton("⬅️ Ortga", callback_data='back_to_voices')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="⚙️ **Sozlamalar:**\n"
                 "Ovoz parametrlarini sozlang:",
            reply_markup=reply_markup
        )
        return
    
    elif query.data == 'back_to_voices':
        # Ovozlar menyusiga qaytish
        await start(query, context)
        return
    
    elif query.data == 'speed_menu':
        # Tezlik menyusi
        keyboard = [
            [InlineKeyboardButton("🐌 Sekin (-50%)", callback_data='speed_-50%')],
            [InlineKeyboardButton("🐢 Bir oz sekin (-25%)", callback_data='speed_-25%')],
            [InlineKeyboardButton("⚖️ Normal", callback_data='speed_+0%')],
            [InlineKeyboardButton("🐇 Bir oz tez (+25%)", callback_data='speed_+25%')],
            [InlineKeyboardButton("⚡ Tez (+50%)", callback_data='speed_+50%')],
            [InlineKeyboardButton("⬅️ Ortga", callback_data='settings')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="⏩ **Tezlikni tanlang:**\n"
                 "(100% = normal tezlik)",
            reply_markup=reply_markup
        )
        return
    
    # Tezlik tanlash
    elif query.data.startswith('speed_'):
        speed = query.data.replace('speed_', '')
        
        if user_id not in user_settings:
            user_settings[user_id] = {}
        
        user_settings[user_id]['speed'] = speed
        
        speed_names = {
            '-50%': '🐌 Sekin (-50%)',
            '-25%': '🐢 Bir oz sekin (-25%)',
            '+0%': '⚖️ Normal',
            '+25%': '🐇 Bir oz tez (+25%)',
            '+50%': '⚡ Tez (+50%)'
        }
        
        await query.edit_message_text(
            text=f"✅ **Tezlik sozlandi:** {speed_names.get(speed, speed)}\n\n"
                 "Endi matn yuboring:",
            parse_mode='Markdown'
        )
        return
    
    # Ovoz tanlash
    if query.data in VOICES:
        voice_code, voice_name, flag = VOICES[query.data]
        
        # Foydalanuvchi sozlamalarini yangilash/yaratish
        if user_id not in user_settings:
            user_settings[user_id] = {
                'voice': voice_code,
                'voice_name': f"{flag} {voice_name}",
                'speed': '+0%'
            }
        else:
            user_settings[user_id]['voice'] = voice_code
            user_settings[user_id]['voice_name'] = f"{flag} {voice_name}"
        
        # O'zbek ovozlari uchun maxsus xabar
        if 'uz-UZ' in voice_code:
            sample_texts = [
                "Salom! Bu O'zbek tilidagi ovoz sinovi.",
                "Texnologiya hayotimizni har kuni osonlashtiradi.",
                "Yangi tillar o'rganish yangi imkoniyatlar ochadi."
            ]
            
            sample_text = "\n".join([f"• {text}" for text in sample_texts])
            
            await query.edit_message_text(
                text=f"✅ **{flag} {voice_name} ovozi tanlandi!**\n\n"
                     f"📝 **O'zbekcha test matnlari:**\n{sample_text}\n\n"
                     f"Endi o'zingiz matn yuboring yoki yuqoridagi matnlardan birini ko'chirib yuboring.",
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(
                text=f"✅ **{flag} {voice_name} ovozi tanlandi!**\n\n"
                     f"Endi matn yuboring:",
                parse_mode='Markdown'
            )
    else:
        await query.edit_message_text("❌ Noma'lum tanlov")

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Matn qabul qilganda - audio yaratish"""
    user_id = update.message.from_user.id
    text = update.message.text.strip()
    
    # Tekshirishlar
    if not text:
        await update.message.reply_text("❌ Matn bo'sh!")
        return
    
    if len(text) > 3000:
        await update.message.reply_text("❌ Matn juda uzun! Maksimum 3000 belgi.")
        return
    
    # Foydalanuvchi sozlamalarini tekshirish
    if user_id not in user_settings or 'voice' not in user_settings[user_id]:
        await update.message.reply_text(
            "⚠️ Avval ovoz tanlashingiz kerak!\n"
            "/start buyrug'idan foydalaning."
        )
        return
    
    settings = user_settings[user_id]
    
    # Audio yaratish
    processing_msg = await update.message.reply_text(
        "🔊 **Audio yaratilmoqda...**",
        parse_mode='Markdown'
    )
    
    try:
        # Sozlamalarni olish
        voice = settings.get('voice', 'uz-UZ-MadinaNeural')  # O'zbek ovozini default qilamiz
        speed = settings.get('speed', '+0%')
        
        print(f"🎙️ Ovoz: {voice}")
        print(f"⏩ Tezlik: {speed}")
        print(f"📝 Matn: {text[:100]}...")
        
        # edge_tts dan foydalanish
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=speed
        )
        
        # Audio faylni yaratish
        filename = f"audio_{user_id}.mp3"
        
        await communicate.save(filename)
        
        print(f"✅ Audio fayl yaratildi: {filename}")
        
        # Faylni yuborish
        with open(filename, 'rb') as audio_file:
            caption = f"🎙️ **Ovoz:** {settings.get('voice_name', 'Oʻzbek ovoz')}\n"
            caption += f"⏩ **Tezlik:** {speed}\n\n"
            caption += f"📄 **Matn:** {text[:100]}..."
            
            if len(text) > 100:
                caption += "..."
            
            await update.message.reply_audio(
                audio=audio_file,
                title=f"TTS: {text[:30]}...",
                performer="TTS Bot",
                caption=caption,
                parse_mode='Markdown'
            )
        
        # Faylni o'chirish
        if os.path.exists(filename):
            os.remove(filename)
            print(f"🗑️ Fayl o'chirildi: {filename}")
        
        # Yana matn so'rash
        await update.message.reply_text(
            "📝 **Yana matn yuboring yoki /start bilan yangi ovoz tanlang.**",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Xatolik: {error_msg}")
        
        # Xatolik tahlili
        if "no audio was received" in error_msg.lower():
            await update.message.reply_text(
                "❌ **Audio yaratib bo'lmadi!**\n\n"
                "Sabablari:\n"
                "• Matn ovoz tiliga mos kelmadi\n"
                "• Serverda muammo\n\n"
                "✅ **Yechim:**\n"
                "• Qisqaroq matn yuboring\n"
                "• Boshqa ovoz tanlang\n"
                "• Matnda faqat oddiy belgilar qoldiring"
            )
        else:
            await update.message.reply_text(f"❌ Xatolik: {error_msg[:150]}")
    
    # Kutish xabarini o'chirish
    try:
        await processing_msg.delete()
    except:
        pass

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test buyrug'i - har bir til uchun matn namunalarini ko'rsatish"""
    test_texts = """
🎙️ **TEST MATNLARI (Har bir til uchun):**

🇺🇸 **INGLIZCHA:**
• Hello! Welcome to our Text-to-Speech bot.
• The quick brown fox jumps over the lazy dog.

🇷🇺 **RUSCHA:**
• Привет! Добро пожаловать в наш бот Text-to-Speech.
• Съешь ещё этих мягких французских булок, да выпей чаю.

🇪🇸 **ISPANCHA:**
• ¡Hola! Bienvenido a nuestro bot de Text-to-Speech.
• El veloz murciélago hindú comía feliz cardillo y kiwi.

🇫🇷 **FRANSUZCHA:**
• Bonjour! Bienvenue dans notre bot Text-to-Speech.
• Portez ce vieux whisky au juge blond qui fume.

🇩🇪 **NEMISCHA:**
• Hallo! Willkommen bei unserem Text-to-Speech-Bot.
• Zwölf Boxkämpfer jagen Viktor quer über den großen Sylter Deich.

🇯🇵 **YAPONCHA:**
• こんにちは！ Text-to-Speech ボットへようこそ。
• 色は匂へど散りぬるを我が世誰ぞ常ならむ有為の奥山今日越えて浅き夢見じ酔ひもせず。

🇰🇷 **KOREYSCHA:**
• 안녕하세요! Text-to-Speech 봇에 오신 것을 환영합니다.
• 키스의 고유조건은 입술끼리 만나야 하고 특별한 기술은 필요치 않다.

🇹🇷 **TURKCHA:**
• Merhaba! Text-to-Speech botumuza hoş geldiniz.
• Pijamalı hasta yağız şoföre çabucak güvendi.

🇺🇿 **OʻZBEKCHA:**
• Salom! Text-to-Speech botimizga xush kelibsiz.
• Juda qiziq, tez va faol boʻlgan tulki haqida hikoya.
• Oʻzbekiston — buyuk kelajakka ega davlat.
• Texnologiya hayotimizni har kuni osonlashtiradi.

📝 **Qoʻllash:** Ovoz tanlang, keyin yuqoridagi matnlardan birini koʻchirib yuboring.
"""
    
    await update.message.reply_text(test_texts, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam"""
    help_text = """
🎙️ **Text-to-Speech Bot (Oʻzbek tili qoʻshildi!)**

**Qoʻllanma:**
1. /start - Ovoz tanlang
2. Matn yuboring (har qanday til)
3. Audio faylni oling

**Buyruqlar:**
/start - Ovoz tanlash
/test - Test matnlarini koʻrish
/help - Yordam

**Qoʻllab-quvvatlanadigan tillar:**
🇺🇸 Inglizcha, 🇷🇺 Ruscha, 🇪🇸 Ispancha
🇫🇷 Fransuzcha, 🇩🇪 Nemischa, 🇯🇵 Yaponcha
🇰🇷 Koreyscha, 🇹🇷 Turkcha, 🇺🇿 Oʻzbekcha

**⚠️ Eslatma:** Har bir ovoz oʻz tilidagi matnlarni yaxshiroq oʻqiydi.
Murojaat uchun: @BugHunter200
"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def uzbek_samples(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'zbekcha matn namunalari"""
    samples = """
🇺🇿 **OʻZBEKCHA TEST MATNLARI:**

1. **Oddiy salom:**
Salom! Text-to-Speech botimizga xush kelibsiz.

2. **Tonggi hayrlash:**
Xayrli tong! Bugun ob-havo juda yaxshi.

3. **Ma'lumot:**
Oʻzbekiston Markaziy Osiyoda joylashgan davlat.

4. **Texnologiya:**
Sun'iy intellext kelajakda koʻplab sohalarni oʻzgartiradi.

5. **Madaniyat:**
Navroʻz — bahor bayrami, yangi yilning boshlanishi.

6. **Iqtisod:**
Yashil iqtisodiyot — barqaror rivojlanishning kaliti.

7. **Ta'lim:**
Bilim — bu hayotdagi eng qimmatbaho boylik.

8. **Sog'liq:**
Sport va toʻgʻri ovqatlanish sogʻlom hayotning asosidir.

📝 **Qoʻllash:** Oʻzbek ovozini tanlang, keyin yuqoridagi matnlardan birini yuboring.
"""
    
    await update.message.reply_text(samples, parse_mode='Markdown')

def main():
    """Asosiy dastur"""
    # Terminalda test matnlarini chiqarish
    print_text_samples()
    
    print("\n🎙️ O'ZBEK TILI QO'SHILGAN TTS BOT")
    print("=" * 50)
    print("🇺🇿 O'zbek ovozlari:")
    print("• uz-UZ-MadinaNeural - Oʻzbek ayol ovoz")
    print("• uz-UZ-SardorNeural - Oʻzbek erkak ovoz")
    print("=" * 50)
    
    try:
        app = Application.builder().token(TOKEN).build()
        
        # Handler'lar
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("test", test_command))
        app.add_handler(CommandHandler("uzbek", uzbek_samples))
        app.add_handler(CommandHandler("help", help_command))
        
        # Callback handler
        app.add_handler(CallbackQueryHandler(button_handler))
        
        # Matn handler
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
        
        print("\n✅ Bot muvaffaqiyatli yuklandi!")
        print("📱 Telegramda oching va /start ni bosing")
        print("🇺🇿 O'zbek ovozlarini sinab ko'ring!")
        print("=" * 50)
        
        app.run_polling()
        
    except Exception as e:
        print(f"❌ Xatolik: {e}")

if __name__ == '__main__':
    main()