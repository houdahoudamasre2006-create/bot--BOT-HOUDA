const Telegram = require('telegram');

// بيانات الـ API الخاصة بك
const client = new Telegram({
  apiId: 32910247,  // استبدل بـ apiId الخاص بك
  apiHash: '1NNFu5dkz2AssKNdNSUeX5WYSqxkMABBjZ',  // استبدل بـ apiHash الخاص بك
  phoneNumber: '+201125603501',  // استبدل بـ رقم الهاتف الخاص بك
  password: 'houdahouda2006houdahouda',  // كلمة مرور 2FA (إن وجدت)
});

// بدء الاتصال بـ Telegram
client.start().then(() => {
  console.log('تم الاتصال بنجاح!');

  // إرسال رسالة إلى المستخدم @Mahamido
  client.sendMessage('@Mahamido', 'تم تشغيل البوت بنجاح!').then(() => {
    console.log('تم إرسال الرسالة إلى @Mahamido بنجاح!');
  }).catch((err) => {
    console.error('حدث خطأ أثناء إرسال الرسالة:', err);
  });

  // إرسال رسالة إلى نفسك (حسابك)
  client.sendMessage('me', 'مرحبًا! هذه رسالة اختبار من البوت.').then(() => {
    console.log('تم إرسال الرسالة إلى نفسك بنجاح!');
  }).catch((err) => {
    console.error('حدث خطأ أثناء إرسال الرسالة إلى نفسك:', err);
  });
}).catch((err) => {
  console.error('حدث خطأ أثناء الاتصال بـ Telegram:', err);
});
