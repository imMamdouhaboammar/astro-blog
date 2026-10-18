---
title: "وهنا بدأت أفهم Contract Drift بشكل عملي جدًا"
description: "قبل ما ألحق أجيب الـReal Data، الـStatistical Tests وقفتني عند الباب وقالتلي تعالى يا حبيبي، عندك Tool بتقول عليها Stable وهي بتقع من Request سليمة جدًا"
pubDatetime: 2026-10-17T12:15:00Z
draft: false
tags:
  - PyMC Marketing
  - Calibration
  - Contract Drift
  - Statistical Tests
  - Schema
  - Lineage
category: "ai-machine-learning"
featured: false
heroImage: "/assets/pymc-marketing/part-4.png"
seriesImage: "/assets/pymc-marketing/cover.jpeg"
ogImage: "/assets/pymc-marketing/part-4.png"
---

طيب فاكر آخر البوست اللي فات لما قلتلك إن اللي جاي Real Dataset بقى، messy data، Promotions ناقصة، Channels داخلة في بعض، وكل واحد داخل الـMeeting مقتنع من قبل الـAnalysis إن الـChannel بتاعته هي اللي شايلة الشركة؟

حلو، أنا مروحتش هناك أصلًا ![😂][image1]

قبل ما ألحق أجيب الـReal Data، الـStatistical Tests وقفتني عند الباب وقالتلي تعالى يا حبيبي، عندك Tool بتقول عليها Stable وهي بتقع من Request سليمة جدًا

والـTool المرة دي كانت `calibrate_mmm`

فاكر الحتة اللي كنت مبسوط بيها أوي في البوست اللي فات؟

- Data
- Model
- قرار
- Experiment
- Evidence جديدة
- Calibration
- قرار جديد

أنا كنت شايف الـ**Calibration** دي من ألطف أجزاء الفكرة كلها، لأنك بدل ما الـMMM تفضل عايشة طول عمرها على الـHistorical Data بتاعتها، تقدر ترجع لها بنتيجة Experiment حصل فعلًا وتقولها:

بصي يا ستي، إحنا زودنا Spend على Meta في Test معين، والـincremental lift اللي طلع كان كذا، ومعانا Uncertainty حوالي القياس ده بالشكل ده

خدي الـEvidence الجديدة دي معاكي وإنتي بتعيدي الـFit

وبكده الـModel الجديدة يبقى عندها Parent Model واضح، ونعرف إنها نسخة اتعمل لها Calibration، ونحتفظ بالـ**Lineage** عشان بعد شهرين منقعدش نبص على 14 Model ونقول مين فيكم ابن مين يا ولاد ![😄][image2]

كل ده جميل

لحد ما الـNightly Statistical Suite اشتغلت

واتنين Tests وقعوا بنفس الرسالة تقريبًا:

`AttributeError: 'LiftTestMeasurement' object has no attribute 'start'`

وأنا أول ما شفتها قلت أكيد Fixture قديمة، أو Test بتبعت Payload ناقص، أو فيه حاجة تافهة يعني في الـSynthetic Data ما أنا ابن أبويا في الشغلانة دي ![😃][image3]

قوم ايه بقا، طلعت الـRequest سليمة تمامًا حسب الـSchema اللي أنا نفسي عاملها

الـ`LiftTestMeasurement` عندي بتقبل:

- `channel`
- `geo`
- `x`
- `delta_x`
- `delta_y`
- `sigma`
- `description`

تمام كده؟

الـService بقى وهي بتحول الـRequest لـDataFrame عشان تبعتها للـPyMC adapter كانت بتعمل:

`test.start`

و

`test.end`

دول two fields مش موجودين أصلًا ![😄][image4]

يعني الـAgent ممكن يقرأ الـSchema صح 100%

يبعت Payload مطابقة لكل حاجة أنا قايل إنها مطلوبة

الـValidation تعدي

نوصل للـService

والكود عندي يسأل الـObject بمنتهى الثقة:

- فين `start`؟
- فين `end`؟

والـObject يرد عليه تقريبًا:

أنا أول مرة أشوف حضرتك في حياتي

وخلاص، الـCalibration ماتت قبل ما **PyMC Marketing** نفسها تلحق تدخل الحفلة

وده Bug سخيف جدًا على الورق

سطرين تقريبًا هما اللي كشفوا لي القصة كلها

بس قعدت عنده شوية، لأن النوع ده من الـBugs هو بالظبط اللي أنا عامل المشروع كله عشان أقلل فرصته

أنا من البوست الأول وأنا قاعد أقولك:

- مفيش رقم ياخد ثقة زيادة عن الدليل
- مفيش Decision Tool تشتغل قبل الـDiagnostics
- مفيش Agent يخترع Calculation من دماغه
- مفيش Recommendation تعدي لو الـModel مرفوضة

![كشف تعارض الواجهة](/assets/pymc-marketing/part-7.png)

وبعد الحنكشة دي كلها، طلع عندي **Public Contract** بيقول حاجة والـ**Implementation** بتطلب حاجة تانية ![😂][image5]

يا سلام يا أستاذ Governance يا جميل يا سكر أنت

أول Reflex عندي كان سهل جدًا:

- ضيف `start` و`end` للـSchema
- شغل الـTests
- اقفل الـIssue
- عيش حياتك

بس كده أنا باخترع Public Contract عشان أسكت Exception

وأنا أصلًا معرفش لسه هل الـupstream calibration path اللي بدعمه محتاج الحقلين دول بالشكل ده، ولا الـService عندي شايلة Mapping قديمة من Iteration فاتت ومحدش خد باله

وده بالنسبالي Fix خطر جدًا رغم إنه ممكن يخلي الـTest أخضر في خمس دقايق

لأن `start` و`end` هنا مش اسمين والسلام

لو أنا دخلتهم في الـTool Contract، يبقى أي Agent بعد كده هيشوفهم كجزء من معنى الـLift Test

يبقى لازم أعرف:

- هل هما Required فعلًا؟
- Optional؟
- بيمثلوا Experiment Window؟
- ولا الـCalibration اللي أنا بستخدمها أصلًا محتاجة `x` و`delta_x` و`delta_y` و`sigma` ومعاهم الـdimensions وخلاص؟

لو الحقلين ليهم معنى حقيقي في الـupstream API اللي أنا مثبت عليها، يتحطوا Typed ويتعمل لهم Validation ويتوثقوا ويتختبروا

لو ملهمش معنى في الـpath اللي أنا بدعمه، يتشال الوصول ليهم من الـService

إنما أضيف Fields عشان Python تبطل تزعقلي؟

كده أنا هبقى صلحت الـError وبوظت معنى الـTool في نفس الوقت ![😄][image6]

## وهنا بدأت أفهم Contract Drift بشكل عملي جدًا

ممكن كل جزء عندك يبقى شكله صح لو بصيتله لوحدها

- الـSchema موجودة
- الـTool متسجلة
- الـService موجودة
- الـAdapter موجود
- الـDocs بتقول إن عندك Lift Test Calibration
- وعندك Test اسمها كمان:

`test_real_pymc_lift_test_calibration_and_lineage`

تحفة

بس أول ما Request حقيقية مشت من أول الـSchema لحد الـService، اتكشف إن فيه جزئين بيتكلموا لهجتين مختلفتين

والأغرب إن `calibrate_mmm` عندي متسجلة في الـCapability Registry كـ`stable`

وأنا عامل قاعدة إن أي Capability أقول عليها Stable لازم يبقى وراها **Executable Evidence Test**

والـEvidence Test اللي متعلقة بالـCalibration؟

هي نفسها واحدة من الـTests اللي وقعت ![😂][image7]

يعني الـTest هنا قامت بالواجب زيادة شوية

بدل ما تثبتلي إن الـCapability Stable، أثبتتلي إن كلمة Stable على الـCurrent HEAD محتاجة تتراجع

ودي كانت صفعة لطيفة جدًا لفكرة بدأت أكررها مع نفسي في المشروع:

- اسم الـTest مش Evidence
- وجود الـTest مش Evidence
- إن الـTest كانت Green الأسبوع اللي فات مش Evidence للـCommit اللي أنا واقف عليه دلوقتي

الـ**Evidence** هي إن الـpath اللي أنا بادعي إنها شغالة اتنفذت فعلًا على النسخة الحالية وعدت

ودي حتة بدأت تغير عندي طريقة كتابة الـTests نفسها

لأن عندي هنا مستويين محتاجهم مع بعض

واحد سريع جدًا يمسك **Contract Drift** من النوع الأهبل ده

يعني Test تبني `LiftTestMeasurement` من الـPublic Schema، تعديها للـCalibration mapping، وتتأكد إن الكود عمره ما يطلب Field مش معلنة

دي حاجة مينفعش أستنى عليها Sampling وChains وPosterior وقهوة وشاي عشان أكتشف في الآخر إن Python مش لاقية Attribute ![😄][image8]

وبعدها يفضل عندي الـStatistical Test التقيلة

- دي اللي تشغل PyMC Marketing فعلًا
- تضيف الـLift Measurement للـModel
- تعمل Fit
- تطلع Child Model
- تتأكد إن الـParent متلمسش
- وتتأكد إن الـLineage اتسجل صح

لأن نجاح الـMapping لوحده برضه ميقوليش إن الـCalibration علميًا وتنفيذيًا مشت زي ما أنا متوقع

وأنا حاسس إن دي من الحاجات اللي بتبان صغيرة جدًا وإنت بتبني Tools للـAI، بس تأثيرها كبير

- الـLLM هنا ممكن تكون مؤدبة جدًا
- اتبعت الـSchema بالحرف
- مختارتش Tool غلط
- مخترعتش Parameters

ومع ذلك الـflow يقع، لأن الـcontract اللي إنت مديهولها نفسه مش متفق مع الكود اللي وراه

مفيش Prompt هينقذك هنا

حتى لو كتبت:

`Please ensure all lift-test fields are valid before calibration`

هيعمل إيه يعني؟

يخترعلك `start` و`end` من الهوا؟ ![😂][image9]

عشان كده كل شوية برجع لنفس الفكرة من زاوية أضيق

كل حاجة أقدر أحولها من تعليمات للـAgent لحاجة قابلة للفحص في الكود والـSchemas والـTests، بحاول أعملها

أنا كنت قبل كده مركز جدًا على إن الـDecision Tools تقفل لو الـModel فشلت في الـDiagnostics

دلوقتي بقيت شايف إن الرحلة تبدأ بدري عن كده بكتير

- هل الـRequest نفسها لها Contract واضحة؟
- هل الـSchema والـService متفقين؟
- هل الـService والـAdapter متفقين؟
- هل الـCapability اللي مكتوب عليها Stable عندي دليل حي إنها شغالة دلوقتي؟
- هل الـTest بتعدي من الـPublic Interface الفعلية ولا بتلف حوالينها وتختبر جزء مريح من الكود؟

والسؤال الأخير ده تحديدًا وجعني شوية ![😄][image10]

لأن Tests كتير ممكن تخليك مبسوط وهي في الحقيقة بتثبت حاجة أضيق بكتير من الـClaim اللي إنت كاتبها في الـREADME

## وده رجعني تاني لموضوع الثقة اللي واضح إنه بقى Theme السلسلة غصب عني

في الأول كنت بسأل:

أثق في ROAS بتاعة الـDashboard قد إيه؟

بعدها:

أثق في الـModel قد إيه؟

بعدها:

أسمح للـAI ياخد قرار إمتى؟

دلوقتي أنا واقف عند سؤال أرخم:

**أثق في الـTool نفسها منين؟**

لأن إن `calibrate_mmm` موجودة في Menu بتاعة الـAgent سهل

إنها تستقبل Payload صحيحة، وتوصلها لمعنى Statistical صحيح، وتعمل Model جديدة من غير ما تبوظ الـParent، وتفضل قابلة لإعادة الاختبار على الـCurrent Code

أهو ده بقى محتاج شغل أكتر من إني أكتب Function وأحط عليها Decorator وأقول الحمدلله بقى عندنا Calibration ![😄][image11]

وعشان أبقى واضح، دي لسه مش Victory Story

الـIssue عندي مفتوحة كـP1 correctness bug

والمطلوب عندي دلوقتي إني أثبت الأول الـupstream contract اللي أنا عايز أدعمه، وبعدها أخلي الـSchema والـService والـAdapter والـDocs والـTests كلهم متفقين عليه

من غير ما أضيف Fields لمجرد إن Error اختفى

ومن غير ما أوطي معنى كلمة Stable عشان القائمة تبقى شكلها حلو

كنت فاكر إن البوست الرابع هيبقى أول مرة أجيب Real Marketing Data وأوريكوا الـMCP وهي بتتعامل مع القرف الحقيقي

واضح إن القرف الحقيقي وصل لوحده بدري شوية ![😂][image12]

والحلو إن الـStatistical Suite وهي ماشية سابتلي هدية تانية كمان

- Model اتحفظت
- اتعمل لها Reload في Application جديدة
- الـSimulation اشتغلت عادي

أول ما وصلنا لـ`optimize_budget`، الـOptimizer رجعت:

`Positive directional derivative for linesearch`

فدلوقتي وأنا لسه بلم `start` و`end` من الأرض، عندي Budget Optimizer مستنياني في الركن وبيبصلي ![😄][image13]

تقريبًا الـReal Data هتستنى شوية على ما أحل مشاكل أخواتها

PyMC لسه عندها كلام معايا ![🫠][image14]

[image1]: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEVHcEwTrPD/ggH/uB79jgn/nBD/wif/hgP/jAb/mg//wyn2uyf+hwT/gAD7kgr/gQH/viP/gQD/uiD/txz/uiAQqOvEkygftOz/hAL/hgP/gAD/hwT/wCb/uR//fwD/vSPllhDnjAv/uyH/gAAsn8P/vCMYi8b/uiBGoqxGo6wilsohlspfFBZYEhT/mQxmGBf/kgn/8IFsGRf/5GT/oBH9phb/2Eb/3VT/zzb/4l3/6G7/rRjZOUfgVWP/zTRPDhL/widLDBEXGjb+0j3/yC3g3uPm7fry0lYuxfz+tBxyGxm/LTnmoSP/7HYdITY0zP8iwPrzzUGslnuDeFN3ppCKy/OQUR/QjiepLi27KjX0pib/1UHyrx2vRjf24XBlPEKngic3ttZYKS5JSUeym1Kmk1/l5u5THCLz9/3nxkfv7vA4MjT9/v/pzl+vr8TBqkbY4fVoyvaus2yJiqYooekkSW34tSRpHxiBNR2THiV/Hh2YIifglivQMj+0UDHShzDeR1W3XzPOPUxjJBfWpi1YUDhORjPouSmkkjGvlT3GoSY+QUt9YGmUi2DbzHafmm1bqJuZiZWLeDrPw3j22V+okGs4zP7Oz9pisqRCvvVDyft2USSVgTy9vcllR1fE0u86rethW0Kkoq24xeDbukuLhYddobWRrH4Tit1ZrNxEeX8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD75u5rAAAALHRSTlMA/CIiGhLY/v4I+f6DktfaktViVYOgkfmikmJjuxlVovtWkrwc1yPWycjOzuWlS4UAAAENSURBVHheY2YAAWHhH8y8op9ATBYgFjL6/1mKQfXxS+bvDAzMDAzyCsJ/f//5/0lPRejxP6CAkFr4xX9iXHLMzxk47v9mYGLQEz740cfhyWXHH/IBeiIMzMKe7rv+XX5i+EPzzMvnCet+M2pryd/3/3qeheF2BAfrau82xgCv9KK/1/4zMCg+iLx2mWEns8atgj38r//8/fv2/3fd6+xvmd+FfZff/u07EHx7rKjy5Rjzz/evP35kZpbm/87scfj7hp/M/75wMVuzfP/5003pytfHT/4zMzC95LlvrnqP8Z3Uhe+vPzMwMjCwMmn+Yxfnu/XnButnBpAAAwPPbxDJ9fEf2OtgwMkE8jYIAABmZWzz24AAhgAAAABJRU5ErkJggg==
[image2]: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEUAAAD/mw//nhH/nxH/kwr/nBD/rxj/vSL/wif/ohT/ggH/gQH/tx7/uiD/uiD/wyj/uyL/rBf/iwb/lAr/hwT/iwX/wCb/vSP/vST/sxv/nQ//hwT/hAL/gAD/gAD/gAD/wyj/wyn/2Uj/yzL/5GX/1UL/0jz/wif/zjb/31b/qRj/mw3/xyz/41//8IV4HRn/kgn/63b/3VH/52z/iwX/7Xv/21D/4Fr/6XH/7oD/uyH/sRr7/P//hgPw4HtERUa6mVFmFxVqFxWAIxr01FR8ckcVGDPOztjOyMrioSZiMDHw9PyIOh/tpCnp02fMtE1VU0g4NTQbHziXj1scJD+BfV7uyUb564XftjpoXnKUkZinj2OqcSPI0+rS1uXd5PLo7viYWCGPcHlyMhqgfn/UlCjkxkw2OUgcIT7Et29hXUXBt3Ktjz/FpEWacSCfjnu2xeKdnrdZERN3RUiFWl24diuyq7myq7oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQ2ruNAAAAInRSTlMACRkiARLYktb+ktlVg2L317tV14P3u6L7kZFjomK809zcy6Y0FQAAAPBJREFUeF4lj1FLwzAUhe9t0rTdZl1tbRB0k02U4YMi/v8/MBH0bSjMgcJExupKm6RrElP3wYVzz9N3EBw07PXWdm+6jO7iUWM1EPKhLAAB4Ln0mcY0YGdb44o40cF+SAKrorpRrrgEdtMXjIbncctU4w1anW+no6rKcnJv+uD58Jh9EQ9m5uWVwjEiu/ASwTwKsvQVs++EpA/X0U7+1kd8crc4/aRZSkmYnABYbje0MKQaiGqCsmzG6yEVK0HNN9w+gfVhhbgoCuchx0veIuLmaq6WTaf+o+2u5P7cBG/1YRxkMxARPEvdPQeQOJN//gBsH1xV/J4GbgAAAABJRU5ErkJggg==
[image3]: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEUAAAD/mw//nhH/hwP/sBn/jQb/kwr/uiH/xSr/nBD/ggH/wif/ggH/tx7/uiD/uiD/wyj/uyL/rBf/rhj/rxn/iwb/lAr/hwT/hAL/gQH/gQD/wCb/wyj/vSP/nQ//ohL/gAD/2Uj/3FD/zjX/1kL/0jz/5Wb/63j/yzH/wSb/31ZoFhT/6W//7n7/74P/nA55HRn/xyz/4Vr/uyH/kQj/41//8YL/shrOycz8/f//pxTrpCj/lQo0OlgrMFGAHxnEr1P033AjJT362VTpyU7/74U2PmfBn0uylFb/rRjL1erP0d309/2Ze4F3MBo6OT1DRE++smeTjFr/8IbftjqhayRoXnKUkZihjnJdMTDd5PLo7viYWCFcFxiMY2bUlCj/oxWFOR78qSFyGxjawVJ1bUhfVztnYk17eF325Xvcx2TIuGitjz/20kutex62xeLdoiOdnrfs8fuyq7pqLzF3RUjhnSy4diuNPiAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABggO1nAAAAIXRSTlMACRn+Iv0Bkv0SltYiVYNi99e709xV14Ni2tW73KKR+7xL6dFSAAAA7UlEQVR4Xi2PQU+DQBCFZ3agUIHFakobEmOlNjHpzR/QH9+j3nsh2mhiitBI1bJAgV0X9Usmee+d5kPQDCyOedvIPqM+PzqqDkglQgEQwJVXWrwhr+LCbPXge3JUKYnAhX+q9BBJ+2b5RjS2+OGsq5mnujB/Gk5x1PrAFsBMAGU3wCfKngIIZAxoe2uUcbJZPCoJRMNs5e6xKzr32rx/cXaGMwsxxuIC4FmlGEj6nm3tqKES5xU5xaYgVQfB+v1Q18mdOObpyYAsL84vP7XB157Fon/d2o0/lpmcvz6kotfTTKgndP/rr7TLBn/pBx+xX5tVwMfoAAAAAElFTkSuQmCC
[image4]: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEUAAAD/mw//nhH/nxH/kwr/nBD/rxj/vSL/wif/ohT/ggH/gQH/tx7/uiD/uiD/wyj/uyL/rBf/iwb/lAr/hwT/iwX/wCb/vSP/vST/sxv/nQ//hwT/hAL/gAD/gAD/gAD/wyj/wyn/2Uj/yzL/5GX/1UL/0jz/wif/zjb/31b/qRj/mw3/xyz/41//8IV4HRn/kgn/63b/3VH/52z/iwX/7Xv/21D/4Fr/6XH/7oD/uyH/sRr7/P//hgPw4HtERUa6mVFmFxVqFxWAIxr01FR8ckcVGDPOztjOyMrioSZiMDHw9PyIOh/tpCnp02fMtE1VU0g4NTQbHziXj1scJD+BfV7uyUb564XftjpoXnKUkZinj2OqcSPI0+rS1uXd5PLo7viYWCGPcHlyMhqgfn/UlCjkxkw2OUgcIT7Et29hXUXBt3Ktjz/FpEWacSCfjnu2xeKdnrdZERN3RUiFWl24diuyq7myq7oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQ2ruNAAAAInRSTlMACRkiARLYktb+ktlVg2L317tV14P3u6L7kZFjomK809zcy6Y0FQAAAPBJREFUeF4lj1FLwzAUhe9t0rTdZl1tbRB0k02U4YMi/v8/MBH0bSjMgcJExupKm6RrElP3wYVzz9N3EBw07PXWdm+6jO7iUWM1EPKhLAAB4Ln0mcY0YGdb44o40cF+SAKrorpRrrgEdtMXjIbncctU4w1anW+no6rKcnJv+uD58Jh9EQ9m5uWVwjEiu/ASwTwKsvQVs++EpA/X0U7+1kd8crc4/aRZSkmYnABYbje0MKQaiGqCsmzG6yEVK0HNN9w+gfVhhbgoCuchx0veIuLmaq6WTaf+o+2u5P7cBG/1YRxkMxARPEvdPQeQOJN//gBsH1xV/J4GbgAAAABJRU5ErkJggg==
[image5]: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEVHcEwTrPD/ggH/uB79jgn/nBD/wif/hgP/jAb/mg//wyn2uyf+hwT/gAD7kgr/gQH/viP/gQD/uiD/txz/uiAQqOvEkygftOz/hAL/hgP/gAD/hwT/wCb/uR//fwD/vSPllhDnjAv/uyH/gAAsn8P/vCMYi8b/uiBGoqxGo6wilsohlspfFBZYEhT/mQxmGBf/kgn/8IFsGRf/5GT/oBH9phb/2Eb/3VT/zzb/4l3/6G7/rRjZOUfgVWP/zTRPDhL/widLDBEXGjb+0j3/yC3g3uPm7fry0lYuxfz+tBxyGxm/LTnmoSP/7HYdITY0zP8iwPrzzUGslnuDeFN3ppCKy/OQUR/QjiepLi27KjX0pib/1UHyrx2vRjf24XBlPEKngic3ttZYKS5JSUeym1Kmk1/l5u5THCLz9/3nxkfv7vA4MjT9/v/pzl+vr8TBqkbY4fVoyvaus2yJiqYooekkSW34tSRpHxiBNR2THiV/Hh2YIifglivQMj+0UDHShzDeR1W3XzPOPUxjJBfWpi1YUDhORjPouSmkkjGvlT3GoSY+QUt9YGmUi2DbzHafmm1bqJuZiZWLeDrPw3j22V+okGs4zP7Oz9pisqRCvvVDyft2USSVgTy9vcllR1fE0u86rethW0Kkoq24xeDbukuLhYddobWRrH4Tit1ZrNxEeX8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD75u5rAAAALHRSTlMA/CIiGhLY/v4I+f6DktfaktViVYOgkfmikmJjuxlVovtWkrwc1yPWycjOzuWlS4UAAAENSURBVHheY2YAAWHhH8y8op9ATBYgFjL6/1mKQfXxS+bvDAzMDAzyCsJ/f//5/0lPRejxP6CAkFr4xX9iXHLMzxk47v9mYGLQEz740cfhyWXHH/IBeiIMzMKe7rv+XX5i+EPzzMvnCet+M2pryd/3/3qeheF2BAfrau82xgCv9KK/1/4zMCg+iLx2mWEns8atgj38r//8/fv2/3fd6+xvmd+FfZff/u07EHx7rKjy5Rjzz/evP35kZpbm/87scfj7hp/M/75wMVuzfP/5003pytfHT/4zMzC95LlvrnqP8Z3Uhe+vPzMwMjCwMmn+Yxfnu/XnButnBpAAAwPPbxDJ9fEf2OtgwMkE8jYIAABmZWzz24AAhgAAAABJRU5ErkJggg==
[image6]: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEUAAAD/mw//nhH/nxH/kwr/nBD/rxj/vSL/wif/ohT/ggH/gQH/tx7/uiD/uiD/wyj/uyL/rBf/iwb/lAr/hwT/iwX/wCb/vSP/vST/sxv/nQ//hwT/hAL/gAD/gAD/gAD/wyj/wyn/2Uj/yzL/5GX/1UL/0jz/wif/zjb/31b/qRj/mw3/xyz/41//8IV4HRn/kgn/63b/3VH/52z/iwX/7Xv/21D/4Fr/6XH/7oD/uyH/sRr7/P//hgPw4HtERUa6mVFmFxVqFxWAIxr01FR8ckcVGDPOztjOyMrioSZiMDHw9PyIOh/tpCnp02fMtE1VU0g4NTQbHziXj1scJD+BfV7uyUb564XftjpoXnKUkZinj2OqcSPI0+rS1uXd5PLo7viYWCGPcHlyMhqgfn/UlCjkxkw2OUgcIT7Et29hXUXBt3Ktjz/FpEWacSCfjnu2xeKdnrdZERN3RUiFWl24diuyq7myq7oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQ2ruNAAAAInRSTlMACRkiARLYktb+ktlVg2L317tV14P3u6L7kZFjomK809zcy6Y0FQAAAPBJREFUeF4lj1FLwzAUhe9t0rTdZl1tbRB0k02U4YMi/v8/MBH0bSjMgcJExupKm6RrElP3wYVzz9N3EBw07PXWdm+6jO7iUWM1EPKhLAAB4Ln0mcY0YGdb44o40cF+SAKrorpRrrgEdtMXjIbncctU4w1anW+no6rKcnJv+uD58Jh9EQ9m5uWVwjEiu/ASwTwKsvQVs++EpA/X0U7+1kd8crc4/aRZSkmYnABYbje0MKQaiGqCsmzG6yEVK0HNN9w+gfVhhbgoCuchx0veIuLmaq6WTaf+o+2u5P7cBG/1YRxkMxARPEvdPQeQOJN//gBsH1xV/J4GbgAAAABJRU5ErkJggg==
[image7]: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEVHcEwTrPD/ggH/uB79jgn/nBD/wif/hgP/jAb/mg//wyn2uyf+hwT/gAD7kgr/gQH/viP/gQD/uiD/txz/uiAQqOvEkygftOz/hAL/hgP/gAD/hwT/wCb/uR//fwD/vSPllhDnjAv/uyH/gAAsn8P/vCMYi8b/uiBGoqxGo6wilsohlspfFBZYEhT/mQxmGBf/kgn/8IFsGRf/5GT/oBH9phb/2Eb/3VT/zzb/4l3/6G7/rRjZOUfgVWP/zTRPDhL/widLDBEXGjb+0j3/yC3g3uPm7fry0lYuxfz+tBxyGxm/LTnmoSP/7HYdITY0zP8iwPrzzUGslnuDeFN3ppCKy/OQUR/QjiepLi27KjX0pib/1UHyrx2vRjf24XBlPEKngic3ttZYKS5JSUeym1Kmk1/l5u5THCLz9/3nxkfv7vA4MjT9/v/pzl+vr8TBqkbY4fVoyvaus2yJiqYooekkSW34tSRpHxiBNR2THiV/Hh2YIifglivQMj+0UDHShzDeR1W3XzPOPUxjJBfWpi1YUDhORjPouSmkkjGvlT3GoSY+QUt9YGmUi2DbzHafmm1bqJuZiZWLeDrPw3j22V+okGs4zP7Oz9pisqRCvvVDyft2USSVgTy9vcllR1fE0u86rethW0Kkoq24xeDbukuLhYddobWRrH4Tit1ZrNxEeX8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD75u5rAAAALHRSTlMA/CIiGhLY/v4I+f6DktfaktViVYOgkfmikmJjuxlVovtWkrwc1yPWycjOzuWlS4UAAAENSURBVHheY2YAAWHhH8y8op9ATBYgFjL6/1mKQfXxS+bvDAzMDAzyCsJ/f//5/0lPRejxP6CAkFr4xX9iXHLMzxk47v9mYGLQEz740cfhyWXHH/IBeiIMzMKe7rv+XX5i+EPzzMvnCet+M2pryd/3/3qeheF2BAfrau82xgCv9KK/1/4zMCg+iLx2mWEns8atgj38r//8/fv2/3fd6+xvmd+FfZff/u07EHx7rKjy5Rjzz/evP35kZpbm/87scfj7hp/M/75wMVuzfP/5003pytfHT/4zMzC95LlvrnqP8Z3Uhe+vPzMwMjCwMmn+Yxfnu/XnButnBpAAAwPPbxDJ9fEf2OtgwMkE8jYIAABmZWzz24AAhgAAAABJRU5ErkJggg==
[image8]: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEUAAAD/mw//nhH/nxH/kwr/nBD/rxj/vSL/wif/ohT/ggH/gQH/tx7/uiD/uiD/wyj/uyL/rBf/iwb/lAr/hwT/iwX/wCb/vSP/vST/sxv/nQ//hwT/hAL/gAD/gAD/gAD/wyj/wyn/2Uj/yzL/5GX/1UL/0jz/wif/zjb/31b/qRj/mw3/xyz/41//8IV4HRn/kgn/63b/3VH/52z/iwX/7Xv/21D/4Fr/6XH/7oD/uyH/sRr7/P//hgPw4HtERUa6mVFmFxVqFxWAIxr01FR8ckcVGDPOztjOyMrioSZiMDHw9PyIOh/tpCnp02fMtE1VU0g4NTQbHziXj1scJD+BfV7uyUb564XftjpoXnKUkZinj2OqcSPI0+rS1uXd5PLo7viYWCGPcHlyMhqgfn/UlCjkxkw2OUgcIT7Et29hXUXBt3Ktjz/FpEWacSCfjnu2xeKdnrdZERN3RUiFWl24diuyq7myq7oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQ2ruNAAAAInRSTlMACRkiARLYktb+ktlVg2L317tV14P3u6L7kZFjomK809zcy6Y0FQAAAPBJREFUeF4lj1FLwzAUhe9t0rTdZl1tbRB0k02U4YMi/v8/MBH0bSjMgcJExupKm6RrElP3wYVzz9N3EBw07PXWdm+6jO7iUWM1EPKhLAAB4Ln0mcY0YGdb44o40cF+SAKrorpRrrgEdtMXjIbncctU4w1anW+no6rKcnJv+uD58Jh9EQ9m5uWVwjEiu/ASwTwKsvQVs++EpA/X0U7+1kd8crc4/aRZSkmYnABYbje0MKQaiGqCsmzG6yEVK0HNN9w+gfVhhbgoCuchx0veIuLmaq6WTaf+o+2u5P7cBG/1YRxkMxARPEvdPQeQOJN//gBsH1xV/J4GbgAAAABJRU5ErkJggg==
[image9]: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEVHcEwTrPD/ggH/uB79jgn/nBD/wif/hgP/jAb/mg//wyn2uyf+hwT/gAD7kgr/gQH/viP/gQD/uiD/txz/uiAQqOvEkygftOz/hAL/hgP/gAD/hwT/wCb/uR//fwD/vSPllhDnjAv/uyH/gAAsn8P/vCMYi8b/uiBGoqxGo6wilsohlspfFBZYEhT/mQxmGBf/kgn/8IFsGRf/5GT/oBH9phb/2Eb/3VT/zzb/4l3/6G7/rRjZOUfgVWP/zTRPDhL/widLDBEXGjb+0j3/yC3g3uPm7fry0lYuxfz+tBxyGxm/LTnmoSP/7HYdITY0zP8iwPrzzUGslnuDeFN3ppCKy/OQUR/QjiepLi27KjX0pib/1UHyrx2vRjf24XBlPEKngic3ttZYKS5JSUeym1Kmk1/l5u5THCLz9/3nxkfv7vA4MjT9/v/pzl+vr8TBqkbY4fVoyvaus2yJiqYooekkSW34tSRpHxiBNR2THiV/Hh2YIifglivQMj+0UDHShzDeR1W3XzPOPUxjJBfWpi1YUDhORjPouSmkkjGvlT3GoSY+QUt9YGmUi2DbzHafmm1bqJuZiZWLeDrPw3j22V+okGs4zP7Oz9pisqRCvvVDyft2USSVgTy9vcllR1fE0u86rethW0Kkoq24xeDbukuLhYddobWRrH4Tit1ZrNxEeX8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD75u5rAAAALHRSTlMA/CIiGhLY/v4I+f6DktfaktViVYOgkfmikmJjuxlVovtWkrwc1yPWycjOzuWlS4UAAAENSURBVHheY2YAAWHhH8y8op9ATBYgFjL6/1mKQfXxS+bvDAzMDAzyCsJ/f//5/0lPRejxP6CAkFr4xX9iXHLMzxk47v9mYGLQEz740cfhyWXHH/IBeiIMzMKe7rv+XX5i+EPzzMvnCet+M2pryd/3/3qeheF2BAfrau82xgCv9KK/1/4zMCg+iLx2mWEns8atgj38r//8/fv2/3fd6+xvmd+FfZff/u07EHx7rKjy5Rjzz/evP35kZpbm/87scfj7hp/M/75wMVuzfP/5003pytfHT/4zMzC95LlvrnqP8Z3Uhe+vPzMwMjCwMmn+Yxfnu/XnButnBpAAAwPPbxDJ9fEf2OtgwMkE8jYIAABmZWzz24AAhgAAAABJRU5ErkJggg==
[image10]: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEUAAAD/mw//nhH/nxH/kwr/nBD/rxj/vSL/wif/ohT/ggH/gQH/tx7/uiD/uiD/wyj/uyL/rBf/iwb/lAr/hwT/iwX/wCb/vSP/vST/sxv/nQ//hwT/hAL/gAD/gAD/gAD/wyj/wyn/2Uj/yzL/5GX/1UL/0jz/wif/zjb/31b/qRj/mw3/xyz/41//8IV4HRn/kgn/63b/3VH/52z/iwX/7Xv/21D/4Fr/6XH/7oD/uyH/sRr7/P//hgPw4HtERUa6mVFmFxVqFxWAIxr01FR8ckcVGDPOztjOyMrioSZiMDHw9PyIOh/tpCnp02fMtE1VU0g4NTQbHziXj1scJD+BfV7uyUb564XftjpoXnKUkZinj2OqcSPI0+rS1uXd5PLo7viYWCGPcHlyMhqgfn/UlCjkxkw2OUgcIT7Et29hXUXBt3Ktjz/FpEWacSCfjnu2xeKdnrdZERN3RUiFWl24diuyq7myq7oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQ2ruNAAAAInRSTlMACRkiARLYktb+ktlVg2L317tV14P3u6L7kZFjomK809zcy6Y0FQAAAPBJREFUeF4lj1FLwzAUhe9t0rTdZl1tbRB0k02U4YMi/v8/MBH0bSjMgcJExupKm6RrElP3wYVzz9N3EBw07PXWdm+6jO7iUWM1EPKhLAAB4Ln0mcY0YGdb44o40cF+SAKrorpRrrgEdtMXjIbncctU4w1anW+no6rKcnJv+uD58Jh9EQ9m5uWVwjEiu/ASwTwKsvQVs++EpA/X0U7+1kd8crc4/aRZSkmYnABYbje0MKQaiGqCsmzG6yEVK0HNN9w+gfVhhbgoCuchx0veIuLmaq6WTaf+o+2u5P7cBG/1YRxkMxARPEvdPQeQOJN//gBsH1xV/J4GbgAAAABJRU5ErkJggg==
[image11]: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEUAAAD/mw//nhH/nxH/kwr/nBD/rxj/vSL/wif/ohT/ggH/gQH/tx7/uiD/uiD/wyj/uyL/rBf/iwb/lAr/hwT/iwX/wCb/vSP/vST/sxv/nQ//hwT/hAL/gAD/gAD/gAD/wyj/wyn/2Uj/yzL/5GX/1UL/0jz/wif/zjb/31b/qRj/mw3/xyz/41//8IV4HRn/kgn/63b/3VH/52z/iwX/7Xv/21D/4Fr/6XH/7oD/uyH/sRr7/P//hgPw4HtERUa6mVFmFxVqFxWAIxr01FR8ckcVGDPOztjOyMrioSZiMDHw9PyIOh/tpCnp02fMtE1VU0g4NTQbHziXj1scJD+BfV7uyUb564XftjpoXnKUkZinj2OqcSPI0+rS1uXd5PLo7viYWCGPcHlyMhqgfn/UlCjkxkw2OUgcIT7Et29hXUXBt3Ktjz/FpEWacSCfjnu2xeKdnrdZERN3RUiFWl24diuyq7myq7oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQ2ruNAAAAInRSTlMACRkiARLYktb+ktlVg2L317tV14P3u6L7kZFjomK809zcy6Y0FQAAAPBJREFUeF4lj1FLwzAUhe9t0rTdZl1tbRB0k02U4YMi/v8/MBH0bSjMgcJExupKm6RrElP3wYVzz9N3EBw07PXWdm+6jO7iUWM1EPKhLAAB4Ln0mcY0YGdb44o40cF+SAKrorpRrrgEdtMXjIbncctU4w1anW+no6rKcnJv+uD58Jh9EQ9m5uWVwjEiu/ASwTwKsvQVs++EpA/X0U7+1kd8crc4/aRZSkmYnABYbje0MKQaiGqCsmzG6yEVK0HNN9w+gfVhhbgoCuchx0veIuLmaq6WTaf+o+2u5P7cBG/1YRxkMxARPEvdPQeQOJN//gBsH1xV/J4GbgAAAABJRU5ErkJggg==
[image12]: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEVHcEwTrPD/ggH/uB79jgn/nBD/wif/hgP/jAb/mg//wyn2uyf+hwT/gAD7kgr/gQH/viP/gQD/uiD/txz/uiAQqOvEkygftOz/hAL/hgP/gAD/hwT/wCb/uR//fwD/vSPllhDnjAv/uyH/gAAsn8P/vCMYi8b/uiBGoqxGo6wilsohlspfFBZYEhT/mQxmGBf/kgn/8IFsGRf/5GT/oBH9phb/2Eb/3VT/zzb/4l3/6G7/rRjZOUfgVWP/zTRPDhL/widLDBEXGjb+0j3/yC3g3uPm7fry0lYuxfz+tBxyGxm/LTnmoSP/7HYdITY0zP8iwPrzzUGslnuDeFN3ppCKy/OQUR/QjiepLi27KjX0pib/1UHyrx2vRjf24XBlPEKngic3ttZYKS5JSUeym1Kmk1/l5u5THCLz9/3nxkfv7vA4MjT9/v/pzl+vr8TBqkbY4fVoyvaus2yJiqYooekkSW34tSRpHxiBNR2THiV/Hh2YIifglivQMj+0UDHShzDeR1W3XzPOPUxjJBfWpi1YUDhORjPouSmkkjGvlT3GoSY+QUt9YGmUi2DbzHafmm1bqJuZiZWLeDrPw3j22V+okGs4zP7Oz9pisqRCvvVDyft2USSVgTy9vcllR1fE0u86rethW0Kkoq24xeDbukuLhYddobWRrH4Tit1ZrNxEeX8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD75u5rAAAALHRSTlMA/CIiGhLY/v4I+f6DktfaktViVYOgkfmikmJjuxlVovtWkrwc1yPWycjOzuWlS4UAAAENSURBVHheY2YAAWHhH8y8op9ATBYgFjL6/1mKQfXxS+bvDAzMDAzyCsJ/f//5/0lPRejxP6CAkFr4xX9iXHLMzxk47v9mYGLQEz740cfhyWXHH/IBeiIMzMKe7rv+XX5i+EPzzMvnCet+M2pryd/3/3qeheF2BAfrau82xgCv9KK/1/4zMCg+iLx2mWEns8atgj38r//8/fv2/3fd6+xvmd+FfZff/u07EHx7rKjy5Rjzz/evP35kZpbm/87scfj7hp/M/75wMVuzfP/5003pytfHT/4zMzC95LlvrnqP8Z3Uhe+vPzMwMjCwMmn+Yxfnu/XnButnBpAAAwPPbxDJ9fEf2OtgwMkE8jYIAABmZWzz24AAhgAAAABJRU5ErkJggg==
[image13]: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEUAAAD/mw//nhH/nxH/kwr/nBD/rxj/vSL/wif/ohT/ggH/gQH/tx7/uiD/uiD/wyj/uyL/rBf/iwb/lAr/hwT/iwX/wCb/vSP/vST/sxv/nQ//hwT/hAL/gAD/gAD/gAD/wyj/wyn/2Uj/yzL/5GX/1UL/0jz/wif/zjb/31b/qRj/mw3/xyz/41//8IV4HRn/kgn/63b/3VH/52z/iwX/7Xv/21D/4Fr/6XH/7oD/uyH/sRr7/P//hgPw4HtERUa6mVFmFxVqFxWAIxr01FR8ckcVGDPOztjOyMrioSZiMDHw9PyIOh/tpCnp02fMtE1VU0g4NTQbHziXj1scJD+BfV7uyUb564XftjpoXnKUkZinj2OqcSPI0+rS1uXd5PLo7viYWCGPcHlyMhqgfn/UlCjkxkw2OUgcIT7Et29hXUXBt3Ktjz/FpEWacSCfjnu2xeKdnrdZERN3RUiFWl24diuyq7myq7oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQ2ruNAAAAInRSTlMACRkiARLYktb+ktlVg2L317tV14P3u6L7kZFjomK809zcy6Y0FQAAAPBJREFUeF4lj1FLwzAUhe9t0rTdZl1tbRB0k02U4YMi/v8/MBH0bSjMgcJExupKm6RrElP3wYVzz9N3EBw07PXWdm+6jO7iUWM1EPKhLAAB4Ln0mcY0YGdb44o40cF+SAKrorpRrrgEdtMXjIbncctU4w1anW+no6rKcnJv+uD58Jh9EQ9m5uWVwjEiu/ASwTwKsvQVs++EpA/X0U7+1kd8crc4/aRZSkmYnABYbje0MKQaiGqCsmzG6yEVK0HNN9w+gfVhhbgoCuchx0veIuLmaq6WTaf+o+2u5P7cBG/1YRxkMxARPEvdPQeQOJN//gBsH1xV/J4GbgAAAABJRU5ErkJggg==
[image14]: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEUAAAD7lRD7nBP6kQ7/qhj5kxH7mBX5ig37lQ7/wij7jQz8nxf6jw/8oRn6kRH6jQ7/uSD/uSD/wSb/shz/qBn6kBD7kxD6kBD/wif6nxn8nhX8mBP7lRP/vSP9rx7/wSf8qR/7nRX+rSH6iAv/wCb/uiD/uB//uB//vCL/rxr+phf4jhD7khD5jhD7hwn/2Ej/3FD/8IT/1UL/uSb+sSL/rR7/zzj/6Gz/zDT/5GX/7oD/xSz/6nP/vyb/0jz/3lX/63f/4l7/yTH/7Hv/qRr/wDH/4Fn/tiH+pBj8mRTqzVT+vStDQ0YqLkyZkFoxOFxZFxA5P2LyuzqCQx53HRjIuWjbx2NtZUfXozI4Nzz721aqgStKDg/Bii+xcCuAdEL03m1UVWAaHTuGfVTMr0tSMhmZax5hLxKPWiJmGBZeExPuqC2Xh0WmnWjxzUuZbSs7CA5OIhLGnjN6Jhq5dy3QjS4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB3DPwfAAAAL3RSTlMAChYcISiSawP+ENFN89QtVpjd3OQ19rzT4cCw5YV99XNA8t+7jWyszMTWqFrtgkBcEL4AAADxSURBVHheLU9RS8MwGPzyJe3adVuybJkURRGkA33y0T/tP/DVJ59loIgdqzCRGmttUrsudsWDO457uOMoHCBOgMfaHSzpmChatkD9V237YMlrgRbG7xjeO6CQSHtknA/VxLT+VxdUkl/SpnaBmZVTplHctNHPODeGKgG+AxZXIPJDfUQpwOmWggo3v7sIPLnjb8BS5tkAz3XhQ4rpYNQQLMgoXCVntRlWV6oZOqqKx7m0sxiC6d6iztCVXHx+P+eTi+M1ueOOIcnZ2smnxW01XzkNmBXyo9zi4qHcE9WtMwAjvGywqTtz/ZL2571e/6//AQ0RXgyfgZFVAAAAAElFTkSuQmCC
