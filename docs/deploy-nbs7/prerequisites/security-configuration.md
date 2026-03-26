---
title: Security
layout: page
parent: AWS prerequisites
nav_order: 5
---

# Security configuration requirements for AWS deployments
{: .no_toc }

## Encryption Management

AWS infrastructure storage services like AWS EBS, EFS, and RDS utilize AWS Key Management Store (KMS) for encryption, ensuring a
robust layer of security.

## End User Authentication

The NBS 7 system will support end user authentication by integrating with a standards-based SSO system. It is designed to be deployed as a protected endpoint within your preexisting SSO ecosystem, and can be configured to work with a wide variety of standards compliant Identity Providers (e.g. Okta, AD).

This is similar to NBS 6. As documented in ["NEDSS Base System Release 4.4.1 Hardening NBS Perimeter Security"](https://nbscentral.cdc.gov/attachments/1995) (requires access on NBS central), NBS 6 does not authenticate users. Instead, it delegates authentication to a security proxy, which each State, Tribal, Local, and Territorial (STLT) must provide in order to deploy NBS.

The NBS 7 release requires that prospective users already have a working NBS 6 instance, and therefore assumes that a user authentication mechanism is already in place.

NBS 7 extends functionality that is available to the authenticated user. NBS 7 therefore works alongside the existing authentication mechanism. No additional steps are needed to authenticate users for NBS 7.

To assist those who are integrating NBS into their SSO ecosystem, a proof of concept in which authentication is performed using an Identity Provider (IdP) and a proxy is available on request. To request it, [please create a ticket here](https://nbscentral.cdc.gov/projects/nbs700/issues/new).
