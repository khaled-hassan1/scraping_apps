import json
# ❌ الخطأ كان هنا: from google_play_scraper import developer
# ✅ التعديل الصحيح:
from google_play_scraper import developer_apps

dev_ids = ["Code Matrix Dev", "K.G. Apps"]
all_apps_data = []

for dev_id in dev_ids:
    print(f"🔄 جاري جلب تطبيقات المطور: {dev_id}...")
    try:
        # استخدام developer_apps بدلاً من developer
        results = developer_apps(dev_id, lang="ar", country="eg")
        
        for app in results:
            all_apps_data.append({
                "id": app.get("appId"),
                "name": app.get("title"),
                "description": app.get("summary") or "تطبيق على متجر جوجل بلاي",
                "iconUrl": app.get("icon"),
                "playStoreUrl": f"https://play.google.com/store/apps/details?id={app.get('appId')}",
            })
        print(f"✅ تم العثور على {len(results)} تطبيق.")
    except Exception as e:
        print(f"❌ حدث خطأ مع المطور {dev_id}: {e}")

# حفظ البيانات في ملف JSON
if all_apps_data:
    with open("apps_data.json", "w", encoding="utf-8") as f:
        json.dump(all_apps_data, f, ensure_ascii=False, indent=4)
    print("\n✨ تم حفظ البيانات بنجاح!")
