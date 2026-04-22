# Incident Report: Payment Gateway Outage

> **Real-world example**: Payment processor downtime affecting checkout

---

## 📋 Incident Overview

| Field | Value |
|-------|-------|
| **Incident ID** | INC-2026-04-15-001 |
| **Date/Time** | 2026-04-15 14:23 UTC |
| **Severity** | 🔴 Critical |
| **Status** | 🟢 Resolved |
| **Duration** | 1 hour 37 minutes |
| **Affected Users** | ~2,500 users (15% of active shoppers) |
| **Business Impact** | $45,000 estimated revenue loss |

---

## 🎯 Summary

**What happened**: Payment gateway integration failed due to expired SSL certificate on our payment proxy service, causing all checkout attempts to fail with timeout errors.

**Impact**: Users unable to complete purchases for 97 minutes during peak shopping hours. 2,500+ affected users, 450+ abandoned carts, estimated $45K revenue loss.

**Resolution**: Renewed SSL certificate and restarted payment proxy service. Implemented automated certificate monitoring.

---

## ⏱️ Timeline

| Time (UTC) | Event | Action Taken |
|------------|-------|--------------|
| 14:23 | 🔴 Incident detected | Datadog alert: Payment success rate dropped to 0% |
| 14:25 | 🔍 Investigation started | On-call engineer paged, war room created |
| 14:28 | 📞 Team assembled | Backend, DevOps, Product teams joined |
| 14:35 | 🔎 Initial hypothesis | Suspected payment provider API issue |
| 14:42 | 📞 Provider contacted | Stripe confirmed their systems operational |
| 14:50 | 🔍 Deep dive logs | Found SSL handshake failures in proxy logs |
| 14:55 | 🔎 Root cause identified | SSL cert expired on payment-proxy service |
| 15:05 | 🔧 Certificate renewed | New cert generated via Let's Encrypt |
| 15:12 | 🚀 Service restarted | payment-proxy pods redeployed |
| 15:18 | ✅ Service restored | Payment success rate back to 99.2% |
| 15:30 | 📊 Monitoring confirmed | All metrics normal for 15 minutes |
| 16:00 | 📝 Post-incident review | Team debrief, action items assigned |

---

## 🔍 Root Cause Analysis

### What Went Wrong

```
Component: payment-proxy service (Node.js microservice)
Failure mode: SSL certificate expiration
Trigger: Certificate expired at 14:22 UTC (90 days after issuance)
```

**Technical details**:
- Payment proxy service uses custom SSL cert for Stripe webhook validation
- Certificate was manually provisioned 90 days ago
- No automated renewal process in place
- No monitoring for certificate expiration
- Service failed silently with generic timeout errors

### Why It Happened

1. **Immediate cause**: SSL certificate expired after 90-day validity period
2. **Contributing factors**: 
   - Manual certificate management process
   - No expiration monitoring/alerts
   - Certificate renewal not in runbook
3. **Underlying issues**: 
   - Lack of infrastructure-as-code for SSL management
   - No automated cert renewal (Let's Encrypt auto-renew disabled)
   - Insufficient observability on SSL handshake failures

### Evidence

```bash
# Error logs from payment-proxy service
[2026-04-15T14:23:15Z] ERROR: SSL handshake failed
  Error: certificate has expired
  at TLSSocket.onConnectSecure (node:_tls_wrap:1530:34)
  
# Stripe webhook delivery failures
[2026-04-15T14:23:20Z] Webhook delivery failed: SSL certificate problem

# Datadog metrics
- payment.success_rate: 99.8% → 0% (14:23)
- payment.timeout_errors: 2/min → 450/min (14:23)
- checkout.completion_rate: 78% → 0% (14:23)
```

---

## 🛠️ Resolution

### Immediate Fix

```bash
# 1. Generate new certificate
certbot certonly --standalone \
  -d payment-proxy.siinstore.com \
  --non-interactive --agree-tos \
  -m devops@siinstore.com

# 2. Update Kubernetes secret
kubectl create secret tls payment-proxy-tls \
  --cert=/etc/letsencrypt/live/payment-proxy.siinstore.com/fullchain.pem \
  --key=/etc/letsencrypt/live/payment-proxy.siinstore.com/privkey.pem \
  --dry-run=client -o yaml | kubectl apply -f -

# 3. Restart service
kubectl rollout restart deployment/payment-proxy -n production
kubectl rollout status deployment/payment-proxy -n production
```

### Deployment

- **Method**: Certificate renewal + rolling restart
- **Deployed by**: DevOps team (John Doe)
- **Deployed at**: 15:12 UTC
- **Verification**: 
  - SSL Labs scan: A+ rating
  - Test payment: Successful
  - Monitoring: Success rate 99.2% for 15 minutes

---

## 📊 Impact Assessment

### User Impact

| Metric | Before | During | After |
|--------|--------|--------|-------|
| Payment success rate | 99.8% | 0% | 99.2% |
| Checkout completion | 78% | 0% | 76% |
| Avg checkout time | 2.3s | N/A (timeout) | 2.1s |
| Error rate | 0.2% | 100% | 0.8% |

### Business Impact

- **Revenue loss**: ~$45,000 (estimated from avg order value × failed checkouts)
- **Affected orders**: 0 completed (450+ attempted)
- **Support tickets**: 127 tickets created
- **User complaints**: 89 social media mentions
- **Cart abandonment**: 450 carts abandoned (recovery email sent)

---

## 🔄 Action Items

### Immediate (0-24h)

- [x] Enable Let's Encrypt auto-renewal - Owner: DevOps - Due: 2026-04-15 ✅
- [x] Send cart recovery emails - Owner: Marketing - Due: 2026-04-15 ✅
- [x] Post status page update - Owner: Support - Due: 2026-04-15 ✅

### Short-term (1-7 days)

- [x] Add SSL cert expiration monitoring - Owner: DevOps - Due: 2026-04-17 ✅
- [x] Create payment service runbook - Owner: Backend - Due: 2026-04-18 ✅
- [ ] Implement cert-manager for K8s - Owner: DevOps - Due: 2026-04-20
- [ ] Add SSL handshake error alerts - Owner: Backend - Due: 2026-04-21

### Long-term (1-4 weeks)

- [ ] Migrate all services to cert-manager - Owner: DevOps - Due: 2026-05-01
- [ ] Implement chaos engineering tests - Owner: SRE - Due: 2026-05-10
- [ ] Add payment failover to backup processor - Owner: Backend - Due: 2026-05-15

---

## 📚 Lessons Learned

### What Went Well

1. **Fast detection**: Datadog alert triggered within 1 minute of failure
2. **Clear escalation**: On-call engineer paged immediately, war room created
3. **Good communication**: Status page updated, users notified via email
4. **Quick resolution**: Root cause identified and fixed within 1 hour

### What Could Be Improved

1. **Prevention**: Should have had automated cert renewal from day 1
2. **Monitoring**: No visibility into SSL cert expiration dates
3. **Error messages**: Generic timeout errors made debugging harder
4. **Documentation**: Certificate renewal not documented in runbook
5. **Testing**: No regular testing of payment flow in staging

### Prevention Measures

1. **Monitoring**: 
   - Datadog SSL cert expiration check (alert 30 days before)
   - PagerDuty alert for cert expiring in < 7 days
   
2. **Testing**: 
   - Weekly automated payment flow tests in staging
   - Quarterly chaos engineering: simulate cert expiration
   
3. **Documentation**: 
   - Payment service runbook updated with cert renewal steps
   - Architecture diagram updated with SSL dependencies
   
4. **Architecture**: 
   - Migrate to cert-manager for automated K8s cert management
   - Implement payment processor failover (Stripe → PayPal)

---

## 🔗 References

- **Monitoring Dashboard**: https://app.datadoghq.com/dashboard/payment-health
- **Error Logs**: https://logs.siinstore.com/payment-proxy/2026-04-15
- **Slack Thread**: #incident-payment-down (2026-04-15)
- **Related Incidents**: None
- **Post-mortem Meeting**: 2026-04-16 10:00 UTC (recording in Notion)

---

## 👥 Response Team

| Role | Name | Contribution |
|------|------|--------------|
| Incident Commander | Jane Smith | Led response, coordinated teams |
| Backend Engineer | John Doe | Identified root cause, deployed fix |
| DevOps Engineer | Alice Johnson | Certificate renewal, K8s deployment |
| Support Lead | Bob Wilson | User communication, status updates |
| Product Manager | Carol Lee | Business impact assessment |

---

## 📝 Communication

### Internal

- **Slack #incidents**: Real-time updates every 10 minutes
- **Email to leadership**: Incident summary sent at 15:30 UTC
- **All-hands mention**: Brief mention in weekly all-hands (2026-04-17)

### External

- **Status page**: "Payment processing experiencing issues" (14:30 UTC)
- **Status page**: "Issue resolved, payments working normally" (15:20 UTC)
- **User email**: Cart recovery email sent to 450 affected users (16:00 UTC)
- **Social media**: Twitter response to 89 user complaints (15:30-17:00 UTC)

---

## ✅ Sign-off

- **Incident Commander**: Jane Smith - 2026-04-16
- **Engineering Lead**: John Doe - 2026-04-16
- **Product Manager**: Carol Lee - 2026-04-16

---

**Template Version**: 1.0
**Incident Type**: Infrastructure / SSL Certificate
**Severity**: Critical
