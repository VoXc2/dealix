export default function RegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4 py-8">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-12 h-12 bg-primary-600 rounded-xl flex items-center justify-center mx-auto mb-4"><span className="text-white font-bold text-xl">D</span></div>
          <h1 className="text-2xl font-bold text-gray-900">إنشاء حساب جديد</h1>
          <p className="text-gray-600 mt-2">انضم إلى Dealix وابدأ إدارة صفقاتك</p>
        </div>
        <div className="card">
          <form className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">الاسم الكامل</label>
              <input type="text" className="input-field" placeholder="محمد أحمد" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">البريد الإلكتروني</label>
              <input type="email" className="input-field" placeholder="example@dealix.sa" dir="ltr" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">رقم الجوال</label>
              <input type="tel" className="input-field" placeholder="05xxxxxxxx" dir="ltr" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">كلمة المرور</label>
              <input type="password" className="input-field" placeholder="8 أحرف على الأقل" dir="ltr" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">نوع الحساب</label>
              <select className="input-field">
                <option value="merchant">تاجر</option>
                <option value="affiliate">مسوّق بالعمولة</option>
                <option value="agency">وكالة</option>
              </select>
            </div>
            <button type="submit" className="btn-primary w-full">إنشاء الحساب</button>
          </form>
          <p className="text-center text-sm text-gray-600 mt-6">لديك حساب؟ <a href="/login" className="text-primary-600 font-medium hover:underline">سجل دخولك</a></p>
        </div>
      </div>
    </div>
  );
}
