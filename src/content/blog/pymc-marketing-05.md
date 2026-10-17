---
title: "دلوقتي واضح عندي إن قرار الميزانية عنده مرحلتين لازم يعدوا"
description: "وطلعت مجهزة لي درس لطيف جدًا في الـCausality جاي أحكيلك عنه"
pubDatetime: 2026-10-17T12:20:00Z
draft: false
tags:
  - PyMC Marketing
  - Budget Optimizer
  - Causality
  - SLSQP
  - Persistence
  - Optimization
category: "ai-machine-learning"
featured: false
heroImage: "/assets/pymc-marketing/part-5.png"
seriesImage: "/assets/pymc-marketing/cover.jpeg"
ogImage: "/assets/pymc-marketing/part-5.png"
---

طيب فاكر الـ**Budget Optimizer** اللي قلتلك في آخر البوست اللي فات إنها مستنياني في الركن هناك كدا وبتبصلي وبتعملي كدا 🤌🏻 بايديها؟

أهو أنا بقا خدت حبايتين شجاعة من بتوع محمد هنيدي في \#أرض_النفاق ورحتلها لغاية عندها😄

وطلعت مجهزة لي درس لطيف جدًا في الـ**Causality** جاي أحكيلك عنه

القصة بدأت من Test اسمها `test_full_persistence_lifecycle_across_restarts`، اسم محترم جدًا يخليك داخل عليها وأنت متوقع تتأكد إن الـModel تعرف تعيش بعد ما الـApplication تقفل وتفتح تاني

الـFlow كان تقريبًا كده: نبني MMM على Synthetic Data، نشغل الـDiagnostics، الـModel تعدي الـDecision Gate، نحفظها، نعمل Application جديدة، نرجع نحمل نفس الـModel، نجرب `simulate_budget` فتشتغل عادي، وبعدها نجرب `optimize_budget` على Budget بـ `150,000` لـ Four Planning Periods

وهنا **PyMC Marketing** قالتلي:

`MinimizeException: Optimization failed: Positive directional derivative for linesearch`

الله ينور يا روح قلبي 😄

أول حاجة دماغي قالتها كانت واضحة جدًا: الـ**Persistence** بوظت حاجة

ما هو الـModel كانت شغالة، اتحفظت، اتعمل لها Reload، وبعدها الـOptimizer وقعت

الــ Case closed يا حضرة المحقق كونان 🤡

بس استنى شوية، أنا أصلًا من أول السلسلة دي قاعد أصدعك بحكاية إن أي إنفاق إعلاني على Meta حصل قبل الـSales لا يثبت أبداً إن Meta هي اللي جابت المبيعات دي.. وإن لو Google ظهر قبل الـConversion لا يخليه ياخد الـCredit كله، وإن وجود event قبل event تاني ميديكش **Causality** هدية

وقوم إيه بقى، لقيت نفسي هتهم الـPersistence لأنها ظهرت في الـTimeline قبل الـFailure 😂

الـTest اسمها Persistence Lifecycle، والـFailure ظهرت بعد Reload، وده Evidence إن المشكلة ظهرت في المسار ده فعلًا

سبب المشكلة نفسه لسه محتاج Experiment أبسط: نفس الـModel، نفس الـBudget، نفس الـPlanning Periods، نفس الـBounds، نشغل الـOptimization قبل الحفظ وبعدين نشغلها بعد الـReload

- لو الاتنين وقعوا بنفس الطريقة، الـPersistence تاخد براءة ونروح نبص على الـFixture أو الـConstraints أو الـOptimizer setup نفسها
- لو اللي قبل الحفظ نجحت واللي بعدها وقعت، ساعتها عندي دليل يستاهل أدخل على الـSerialization والـCoordinates والـdtypes وترتيب الـDimensions والحاجات اللي ممكن تكون اتغيرت أثناء الحفظ والتحميل\>\> ودا عادي علفكرة بيحصل مش أزمة كبيرة يعني

وآه دي حتة عجبتني جدًا لأن الـdebugging هنا رجعني لنفس السؤال بتاع الـ**Marketing Science**: إيه اللي حصل فعلًا؟ وإيه اللي عندي دليل إنه سببه؟

السؤالين قريبين جدًا وإنت بتحكي القصة، إنما القرار اللي هتاخده بعدهم ممكن يروح في حتة أربعتاشر خالص

## خليني أرجع خطوة للـError نفسها .. عشان فيها جزئية كدا مش مفهومة 😄

خلينا متفقين سوا ان **PyMC Marketing** المكتبة نفسها بتعمل **Budget Optimization** كمسألة constrained optimization.. دا تمام

إنت عندك Total Budget، وعندك Channels، وممكن تحط Minimums وMaximums وقيود إضافية، والـOptimizer يحاول يلاقي Allocation تدي Expected Response أعلى تحت القيود دي.. ودا تمام بردو

الـBudget Optimizer في PyMC Marketing بيستخدم **SLSQP**، وده solver للمسائل اللي فيها constraints.. حلو دا.. بس الـ مش حلو بقا اللي جاي 🥴

رسالة `Positive directional derivative for linesearch` معناها عمليًا إن الـsolver وقف ومقدرش يلاقي step مناسبة تكمل بيها الـline search تحت الـobjective والـconstraints بالشكل الحالي

الرسالة دي لوحدها متقوليش السبب

ممكن يبقى عندي مشكلة Scaling، أو الـConstraints عاملة مساحة صعبة جدًا أو مفيهاش حل valid أصلًا، أو الـinitial point وحش، أو حاجة في الـModel state والـcoordinates اتغيرت بعد الـreload، أو الـSynthetic Fixture نفسها بتطلب حاجة صعبة عدديًا

وفيه حتة مهمة هنا أنا شخصيًا كنت محتاج أفصلها في دماغي

نجاح الـ `simulate_budget` بعد الـReload مش بيجبر الـ `optimize_budget` إنها تنجح

- الـ**Simulation** بتاخد Scenario أنت محدده أصلًا وتقيّم الـModel عليه
- الـ**Optimization** عندها شغل تاني خالص، هي بتدور جوه مساحة كبيرة من الـAllocations وتحاول تلاقي واحدة تحقق الهدف وتحترم كل القيود في نفس الوقت

فنجاح الـSimulation دليل مفيد إن الـModel المعمول لها Load قادرة تحسب Response لسيناريو معين\>\> هو دا حلو طبعاً

لكن لسه محتاجين دليل منفصل إن الـOptimization نفسها قادرة تحل المسألة اللي اديناهالها

وعشان كده أسهل Fix هنا هو أكتر واحد مخوفني: أزود retries، أغير tolerance، أبدل initial guess، أجرب seed تانية، أو أغير شوية أرقام في الـFixture لحد ما الـCI تبقى خضرا ونرجع كلنا بيوتنا ننام مرتاحين البال؟

نجاح الـsolver مرة بعد شوية حنكشة ميقوليش إني فهمت السبب

ومع Tool وظيفتها تقولك تحط ملايين فين، أنا محتاج Evidence أحسن من `اشتغلت لما زقيناها خطوتين شوية` 😄 .. دي فلوس ناس يابا

وفيه مثال أبسط يخلي اللي بحكيلك عليه دا واضح

تخيل إنك داخل للـOptimizer وبتقوله الـ Budget كلها مليون، وفي نفس الوقت حاطط Minimum على Meta بـ600 ألف وMinimum على Google بـ500 ألف

أنت كده طلبت منها توزع مليون تحت شروط محتاجة على الأقل 1.1 مليون

مفيش Allocation سحرية هتصلح الكلام ده، والرد المهني هنا إن القيود نفسها غير قابلة للتنفيذ بالشكل الحالي

أي Tool ترجعلك أرقام شكلها مرتب في الحالة دي هتبقى بتديلك Recommendation مريحة بصريًا ومضروبة بالنار رياضيًا

## وده فتحلي Gate جديدة في دماغي فوق الـDecision Gate اللي حكيتلك عنها في البوست الثالث

أنا كنت مركز إن الـModel لازم تعدي الـDiagnostics الأول: Divergences، R-hat، ESS، Posterior Predictive Checks، وكل الحاجات اللي تحدد هل ينفع نسمح للـDecision Tools تشتغل ولا لأ

دلوقتي واضح عندي إن قرار الميزانية عنده مرحلتين لازم يعدوا

**صلاحية الـModel نفسها، وبعدها صلاحية نتيجة الـOptimization**

وده نوع تاني من المشاكل غير الـStatistical Uncertainty اللي كنت بتكلم عنها في أول السلسلة دي

ممكن يبقى عندك Posterior كويسة والـDiagnostics مطمنة، وفي نفس الوقت الـNumerical Solver مقدرتش تحل مسألة الـAllocation اللي طلبتها منها

ساعتها مفيش أي تناقض

- الـModel بتقول إن عندها Evidence تسمح بالحساب
- والـSolver بتقول إن عملية البحث الحالية موصلتش لحل صالح تقدر ترجعهولك

ومن هنا بدأت أبص على Output الـOptimizer نفسها كحاجة محتاجة Evidence

الـsolver رجعت Success فعلًا؟ الـBudget النهائي محفوظ بالكامل؟ كل Channel احترمت الـBounds بتاعتها؟ أي Cell Constraints موجودة اتحققت؟ الـAllocation فيها أرقام finite ومنطقية؟

ولو الـOptimizer فشلت، النتيجة المفيدة هي Failure واضح ومفهوم من غير Allocation تتخيل إنها Recommendation وهي مفترض لأ

ودي نقطة حساسة جدًا مع الـAI تحديدًا لأن الـAgent بطبيعته عايز يكمل الـTask (ويقولك هييييييييه خلصنا "خُد")

إنت قلتله `وزعلي الـBudget`، فهو عايز يرجعلك Budget متوزعة

لو الـTool اللي وراه اديتله Exception خام، عندك كذا احتمال سيئ: الـAgent يحاول retry بطريقة ملهاش أساس، يغير Parameters من عنده، أو يفسر Error تقنية لمستخدم ملوش أي ذنب في SLSQP ومشاكله العائلية 😄

أنا عايز الـBoundary هنا تبقى واضحة

- الـOptimizer قدرت تنتج Allocation صالح تحت القيود المعطاة؟ رجع النتيجة ومعاها الـEvidence اللي تخليني أفهمها
- الـOptimizer مقدرتش؟ رجع Failure ثابت بلغة الـDomain تقول إن مفيش Allocation موثوقة اتولدت، وتحافظ على السبب التقني جوه الـEvidence من غير ما نحول الـFailure لـ Fake Success

والأهم إننا عمرنا ما ناخد الـinitial allocation أو الـhistorical allocation ونرجعها للمستخدم على إنها optimized لمجرد إننا محتاجين Answer

لأن ساعتها الـAI هتكون عملت أسوأ حاجة ممكنة في الـ Analytics: خدت حالة `معرفش` ولبستها رقم وخُد تاني يا يوزر

## وده رجعني لحاجة بدأت تبقى Theme غصب عني في المشروع

في البوست الأول لو تفتكر.. كنت قلقان من ان يكون فيه Attribution الرقم بتاعها واخد ثقة زيادة عن اللزوم، في التاني كنت عايز الـAI تعرف إمتى تطلب Calculation حقيقية، في التالت قفلت الـDecision Tools ورا Diagnostics، وفي الرابع اكتشفت إن الـTool Contract نفسها ممكن تبقى كاتبة حاجة والـImplementation طالبة حاجة تانية

ودلوقتي وصلت لمرحلة أبعد: حتى بعد ما الـData تعدي، والـModel تعدي، والـContract تبقى سليمة، الـNumerical Optimization نفسها ممكن تقولك `أنا مقدرتش أوصل لحل أقدر أدافع عنه`

وده Valid Response جدًا، خصوصًا إن الـOptimization في الحياة الفعلية بتبدأ بقيود Business حقيقية

Meta مينفعش تنزل عن رقم عشان عندك always-on activity، Search لازم يفضل موجود، TikTok عندها Cap عشان لسه Experimental، YouTube فيه Commitment متفق عليه، وفي الآخر عايز Budget واحدة تتوزع وتحقق هدف

كل Constraint بتضيفها بتقلل المساحة اللي الـsolver تقدر تتحرك فيها، وفي لحظة معينة ممكن تكتشف إن الشروط اللي إنت حاططها هي اللي متخانقة مع بعض والـsolver واقفة قدام مسألة مفيهاش مساحة valid تتحرك فيها

وده بالنسبالي مفيد جدًا في الـProduct نفسه

بدل ما الفنكشن `optimize_budget` تكون زرار بيطلع Allocation وخلاص، أنا عايزها تعرف تميز بين كذا حالة: Model مرفوضة، Constraints مش هينفع تتنفذ، Solver مقدرتش توصل للحل، وOptimization نجحت وعدت الـinvariants

لأن كل حالة من دول بالنسبة لواحد داخل Budget Meeting معناها قرار مختلف تماماً

والـIssue عندي لسه مفتوحة كـP1 لحد دلوقتي

أنا لسه معنديش Root Cause مثبتة للـfailure دي، ومفيش قصة بطولة جاهزة هنا

الخطوة اللي تستحق تتعمل دلوقتي بسيطة جدًا في شكلها: نفس الـOptimization قبل الـPersistence وبعدها، وبعدها أقارن الحاجات اللي المفروض تفضل ثابتة وأشوف أول مكان النتيجة اتغيرت عنده

- لو الـpre-reload نجحت والـpost-reload وقعت، هندخل على Persistence ونشوف إيه اللي اتغير
- لو الاتنين وقعوا، هنسيب Persistence في حالها ونروح للـFixture والـBounds والـOptimizer setup

وبعد ما السبب يتثبت، الـFailure نفسها لازم تتحول لحاجة مفهومة تخلي الـAgent يقف هنا.. بدل ما يطلع Recommendation وهو شايف Failure قدامه

وأنا بصراحة مستمتع جدًا إن المشروع كل شوية يرجع يحطني قدام نفس مبادئ الـ**Marketing Science** كل مرة ويرمي في وشي من ناحية تانية حاجات مكنتش متخيل اني ممكن أعرف اتعامل أو أفكر فيها

أنا قاعد أقول من أول يوم متقولش إن حاجة سببت حاجة عشان ظهرت قبلها، وفجأة لقيت Test اسمها Persistence وقعت بعد Reload وكنت هكتب في دماغي `Persistence bug`

حلو يا ممدوح 😄

لحد دلوقتي الإجابة الحقيقية هي: معرفش الـPersistence هي السبب ولا لأ، وعندي Test واضحة هتجاوبني

ودي تقريبًا أحسن حاجة ممكن أقولها عن الـIssue دي حاليًا، لأن لو جاوبت قبل ما أشغل المقارنة هكون بعمل في الـdebugging نفس الحاجة اللي قاعد أهاجمها في الـAttribution من أول بوست

شفت two events ورا بعض وقررت إن واحد سبب التاني

فـ PyMC عندها طرق غريبة جدًا تربي الواحد والله 🫠

مستنيك في بوست تاني اقولك عملت اي ووصلت فين
