# SAMM Container Action Template

This action is not for building Owasp Samm Web page.

To test locally, use:

```
❯ docker build -t process-yaml-content .
❯ cd <owasp samm core>
❯ docker run -v $(pwd)/output:/tmp/output -v $(pwd)/model:/tmp/model -t process-yaml-content:latest -d /tmp/model -o /tmp/output
--- Building SAMM Web markdown
tidying up any leftover files
writing ns files to namespaces
mapping namespaces to templates
creating ./run_make_markdown_script.sh
wrote /build/run_make_web_markdown_script.sh
/build/bin/make_markdown.py /tmp/output/namespaces/Design-SA-A.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Design-SA-A.md
/build/bin/make_markdown.py /tmp/output/namespaces/Design-SA-B.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Design-SA-B.md
/build/bin/make_markdown.py /tmp/output/namespaces/Design-SA.ns /tmp/output/templates/practice.template > /tmp/output/markdown/Design-SA.md
/build/bin/make_markdown.py /tmp/output/namespaces/Design-SR-A.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Design-SR-A.md
/build/bin/make_markdown.py /tmp/output/namespaces/Design-SR-B.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Design-SR-B.md
/build/bin/make_markdown.py /tmp/output/namespaces/Design-SR.ns /tmp/output/templates/practice.template > /tmp/output/markdown/Design-SR.md
/build/bin/make_markdown.py /tmp/output/namespaces/Design-TA-A.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Design-TA-A.md
/build/bin/make_markdown.py /tmp/output/namespaces/Design-TA-B.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Design-TA-B.md
/build/bin/make_markdown.py /tmp/output/namespaces/Design-TA.ns /tmp/output/templates/practice.template > /tmp/output/markdown/Design-TA.md
/build/bin/make_markdown.py /tmp/output/namespaces/Design.ns /tmp/output/templates/function.template > /tmp/output/markdown/Design.md
/build/bin/make_markdown.py /tmp/output/namespaces/Governance-EG-A.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Governance-EG-A.md
/build/bin/make_markdown.py /tmp/output/namespaces/Governance-EG-B.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Governance-EG-B.md
/build/bin/make_markdown.py /tmp/output/namespaces/Governance-EG.ns /tmp/output/templates/practice.template > /tmp/output/markdown/Governance-EG.md
/build/bin/make_markdown.py /tmp/output/namespaces/Governance-PC-A.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Governance-PC-A.md
/build/bin/make_markdown.py /tmp/output/namespaces/Governance-PC-B.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Governance-PC-B.md
/build/bin/make_markdown.py /tmp/output/namespaces/Governance-PC.ns /tmp/output/templates/practice.template > /tmp/output/markdown/Governance-PC.md
/build/bin/make_markdown.py /tmp/output/namespaces/Governance-SM-A.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Governance-SM-A.md
/build/bin/make_markdown.py /tmp/output/namespaces/Governance-SM-B.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Governance-SM-B.md
/build/bin/make_markdown.py /tmp/output/namespaces/Governance-SM.ns /tmp/output/templates/practice.template > /tmp/output/markdown/Governance-SM.md
/build/bin/make_markdown.py /tmp/output/namespaces/Governance.ns /tmp/output/templates/function.template > /tmp/output/markdown/Governance.md
/build/bin/make_markdown.py /tmp/output/namespaces/Implementation-DM-A.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Implementation-DM-A.md
/build/bin/make_markdown.py /tmp/output/namespaces/Implementation-DM-B.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Implementation-DM-B.md
/build/bin/make_markdown.py /tmp/output/namespaces/Implementation-DM.ns /tmp/output/templates/practice.template > /tmp/output/markdown/Implementation-DM.md
/build/bin/make_markdown.py /tmp/output/namespaces/Implementation-SB-A.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Implementation-SB-A.md
/build/bin/make_markdown.py /tmp/output/namespaces/Implementation-SB-B.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Implementation-SB-B.md
/build/bin/make_markdown.py /tmp/output/namespaces/Implementation-SB.ns /tmp/output/templates/practice.template > /tmp/output/markdown/Implementation-SB.md
/build/bin/make_markdown.py /tmp/output/namespaces/Implementation-SD-A.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Implementation-SD-A.md
/build/bin/make_markdown.py /tmp/output/namespaces/Implementation-SD-B.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Implementation-SD-B.md
/build/bin/make_markdown.py /tmp/output/namespaces/Implementation-SD.ns /tmp/output/templates/practice.template > /tmp/output/markdown/Implementation-SD.md
/build/bin/make_markdown.py /tmp/output/namespaces/Implementation.ns /tmp/output/templates/function.template > /tmp/output/markdown/Implementation.md
/build/bin/make_markdown.py /tmp/output/namespaces/Operations-EM-A.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Operations-EM-A.md
/build/bin/make_markdown.py /tmp/output/namespaces/Operations-EM-B.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Operations-EM-B.md
/build/bin/make_markdown.py /tmp/output/namespaces/Operations-EM.ns /tmp/output/templates/practice.template > /tmp/output/markdown/Operations-EM.md
/build/bin/make_markdown.py /tmp/output/namespaces/Operations-IM-A.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Operations-IM-A.md
/build/bin/make_markdown.py /tmp/output/namespaces/Operations-IM-B.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Operations-IM-B.md
/build/bin/make_markdown.py /tmp/output/namespaces/Operations-IM.ns /tmp/output/templates/practice.template > /tmp/output/markdown/Operations-IM.md
/build/bin/make_markdown.py /tmp/output/namespaces/Operations-OM-A.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Operations-OM-A.md
/build/bin/make_markdown.py /tmp/output/namespaces/Operations-OM-B.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Operations-OM-B.md
/build/bin/make_markdown.py /tmp/output/namespaces/Operations-OM.ns /tmp/output/templates/practice.template > /tmp/output/markdown/Operations-OM.md
/build/bin/make_markdown.py /tmp/output/namespaces/Operations.ns /tmp/output/templates/function.template > /tmp/output/markdown/Operations.md
/build/bin/make_markdown.py /tmp/output/namespaces/Verification-AA-A.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Verification-AA-A.md
/build/bin/make_markdown.py /tmp/output/namespaces/Verification-AA-B.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Verification-AA-B.md
/build/bin/make_markdown.py /tmp/output/namespaces/Verification-AA.ns /tmp/output/templates/practice.template > /tmp/output/markdown/Verification-AA.md
/build/bin/make_markdown.py /tmp/output/namespaces/Verification-RT-A.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Verification-RT-A.md
/build/bin/make_markdown.py /tmp/output/namespaces/Verification-RT-B.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Verification-RT-B.md
/build/bin/make_markdown.py /tmp/output/namespaces/Verification-RT.ns /tmp/output/templates/practice.template > /tmp/output/markdown/Verification-RT.md
/build/bin/make_markdown.py /tmp/output/namespaces/Verification-ST-A.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Verification-ST-A.md
/build/bin/make_markdown.py /tmp/output/namespaces/Verification-ST-B.ns /tmp/output/templates/activity.template > /tmp/output/markdown/Verification-ST-B.md
/build/bin/make_markdown.py /tmp/output/namespaces/Verification-ST.ns /tmp/output/templates/practice.template > /tmp/output/markdown/Verification-ST.md
/build/bin/make_markdown.py /tmp/output/namespaces/Verification.ns /tmp/output/templates/function.template > /tmp/output/markdown/Verification.md
runing ./run_make_web_markdown_script.sh
fixing up markdown files..
done
```

Not intended for general use!
