# Incident Report Template

> **Mục đích**: Document production incidents với timeline, root cause, và resolution

---

## 📋 Incident Overview

| Field | Value |
|-------|-------|
| **Incident ID** | INC-[YYYY-MM-DD]-[XXX] |
| **Date/Time** | [YYYY-MM-DD HH:MM UTC] |
| **Severity** | 🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low |
| **Status** | 🔴 Ongoing / 🟡 Investigating / 🟢 Resolved |
| **Duration** | [X hours Y minutes] |
| **Affected Users** | [Number/Percentage] |
| **Business Impact** | [Revenue loss, user complaints, etc.] |

---

## 🎯 Summary

**What happened**: [1-2 câu mô tả incident]

**Impact**: [Tác động đến users/business]

**Resolution**: [Cách đã fix]

---

## ⏱️ Timeline

| Time (UTC) | Event | Action Taken |
|------------|-------|--------------|
| 14:23 | 🔴 Incident detected | Monitoring alert triggered |
| 14:25 | 🔍 Investigation started | Team notified via Slack |
| 14:30 | 🔎 Root cause identified | [Description] |
| 14:45 | 🔧 Fix deployed | [Description] |
| 15:00 | ✅ Service restored | Monitoring confirmed recovery |
| 15:30 | 📊 Post-incident review | Team debrief scheduled |

---

## 🔍 Root Cause Analysis

### What Went Wrong

```
[Detailed technical explanation]
- Component affected: [Service/Module]
- Failure mode: [How it failed]
- Trigger: [What caused the failure]
```

### Why It Happened

1. **Immediate cause**: [Direct trigger]
2. **Contributing factors**: [Conditions that enabled the failure]
3. **Underlying issues**: [Systemic problems]

### Evidence

```bash
# Error logs
[Relevant log entries]

# Metrics
- Error rate: [X%]
- Response time: [Xms]
- Traffic: [X req/s]
```

---

## 🛠️ Resolution

### Immediate Fix

```typescript
// Code changes made
[Relevant code snippets]
```

### Deployment

- **Method**: [Hotfix/Rollback/Config change]
- **Deployed by**: [Name]
- **Deployed at**: [Time]
- **Verification**: [How confirmed fix worked]

---

## 📊 Impact Assessment

### User Impact

| Metric | Before | During | After |
|--------|--------|--------|-------|
| Success rate | 99.9% | 45.2% | 99.9% |
| Avg response time | 120ms | 8500ms | 115ms |
| Error rate | 0.1% | 54.8% | 0.1% |

### Business Impact

- **Revenue loss**: $[X]
- **Affected orders**: [X]
- **Support tickets**: [X]
- **User complaints**: [X]

---

## 🔄 Action Items

### Immediate (0-24h)

- [ ] [Action] - Owner: [Name] - Due: [Date]
- [ ] [Action] - Owner: [Name] - Due: [Date]

### Short-term (1-7 days)

- [ ] [Action] - Owner: [Name] - Due: [Date]
- [ ] [Action] - Owner: [Name] - Due: [Date]

### Long-term (1-4 weeks)

- [ ] [Action] - Owner: [Name] - Due: [Date]
- [ ] [Action] - Owner: [Name] - Due: [Date]

---

## 📚 Lessons Learned

### What Went Well

1. [Positive aspect]
2. [Positive aspect]

### What Could Be Improved

1. [Improvement area]
2. [Improvement area]

### Prevention Measures

1. **Monitoring**: [New alerts/dashboards]
2. **Testing**: [New test cases]
3. **Documentation**: [Updated runbooks]
4. **Architecture**: [System improvements]

---

## 🔗 References

- **Monitoring Dashboard**: [URL]
- **Error Logs**: [URL]
- **Slack Thread**: [URL]
- **Related Incidents**: [INC-XXX, INC-YYY]
- **Post-mortem Meeting**: [Date/Recording]

---

## 👥 Response Team

| Role | Name | Contribution |
|------|------|--------------|
| Incident Commander | [Name] | Led response |
| Engineer | [Name] | Identified root cause |
| Engineer | [Name] | Deployed fix |
| DevOps | [Name] | Infrastructure support |
| Support | [Name] | User communication |

---

## 📝 Communication

### Internal

- **Slack**: [Summary of internal comms]
- **Email**: [Stakeholder notifications]

### External

- **Status page**: [What was posted]
- **User notification**: [Email/In-app message]
- **Social media**: [If applicable]

---

## ✅ Sign-off

- **Incident Commander**: [Name] - [Date]
- **Engineering Lead**: [Name] - [Date]
- **Product Manager**: [Name] - [Date]

---

**Template Version**: 1.0
**Last Updated**: 2026-04-23
