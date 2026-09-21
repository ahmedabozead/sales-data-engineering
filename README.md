# Sales Data Engineering

مشروع بسيط لهندسة بيانات المبيعات باستخدام Python وPandas، يتضمن توليد البيانات، تنظيفها، التحقق من جودتها، وتحميلها إلى SQLite أو SQL Server.

## محتويات المشروع

| المسار | الوصف |
|---|---|
| `data/raw/` | ملفات البيانات الخام |
| `data/clean/` | الملفات الناتجة بعد التنظيف |
| `scripts/` | سكربتات التوليد والتحويل والتحقق والتحميل |
| `database/` | قاعدة SQLite المحلية عند إنشائها |
| `logs/` | سجلات التشغيل المحلية |

## نتيجة تنظيف بيانات المبيعات

تم تنظيف ملف المبيعات بنجاح من أصل **10,003** سجل، وأصبح عدد السجلات النهائية **9,774** سجلًا. شملت المعالجة إزالة التكرارات، القيم الناقصة، المنتجات غير الصالحة، الكميات غير الصحيحة، والتواريخ غير الصالحة.

## المتطلبات

- Python 3.10 أو أحدث
- حزمة ODBC Driver for SQL Server مطلوبة فقط عند استخدام سكربتات SQL Server

## التشغيل

أنشئ بيئة افتراضية وثبّت التبعيات:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

لتشغيل مراحل التحويل والتحقق الأساسية:

```bash
python scripts/transform_customers.py
python scripts/transform_products.py
python scripts/transform_sales.py
python scripts/validate_data.py
```

لتشغيل قاعدة SQLite المحلية:

```bash
python scripts/load_to_database.py
python scripts/validate_database.py
```

> سكربت `run_pipeline.py` يتضمن خطوات SQL Server، لذلك يحتاج إلى إعداد SQL Server وODBC Driver قبل تشغيله كاملًا.

## ملاحظات GitHub

تم استبعاد البيئة الافتراضية، ملفات السجلات، وقواعد البيانات المحلية من Git عبر `.gitignore`. أما ملفات البيانات الخام والمنظفة الموجودة في المشروع فهي جزء من عينة المشروع ويمكن رفعها إذا كان المستودع خاصًا أو كانت البيانات غير حساسة.
