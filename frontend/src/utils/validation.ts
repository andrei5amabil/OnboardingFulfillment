export interface ValidationAlert {
  severity: 'critical' | 'warning' | 'info';
  field: string;
  message: string;
}

export function formatName(name: string | null | undefined): string {
  if (!name || typeof name !== 'string') return '';

  const capitalizePart = (part: string): string => {
    if (!part) return '';
    if (part.toLowerCase().startsWith('mc') && part.length > 2) {
      return 'Mc' + part.charAt(2).toUpperCase() + part.slice(3).toLowerCase();
    }
    return part.charAt(0).toUpperCase() + part.slice(1).toLowerCase();
  };

  const capitalizeToken = (token: string): string => {
    return token.split("'").map(capitalizePart).join("'");
  };

  return name
    .trim()
    .split(/\s+/)
    .map((word) => word.split('-').map(capitalizeToken).join('-'))
    .join(' ');
}

export function validateRomanianCnp(cnp: string | null | undefined): { isValid: boolean; reason: string } {
  if (!cnp) return { isValid: false, reason: 'CNP is missing.' };

  const clean = cnp.replace(/\s+/g, '').trim();
  if (clean.length !== 13 || !/^\d+$/.test(clean)) {
    return { isValid: false, reason: `CNP '${clean}' must be exactly 13 digits.` };
  }

  const CONTROL_KEY = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9];
  const digits = clean.split('').map(Number);

  const checksum = digits.slice(0, 12).reduce((acc, digit, idx) => acc + digit * CONTROL_KEY[idx], 0) % 11;
  const expectedControl = checksum === 10 ? 1 : checksum;

  if (digits[12] !== expectedControl) {
    return { isValid: false, reason: `CNP '${clean}' failed mathematical checksum verification.` };
  }

  return { isValid: true, reason: 'CNP is valid.' };
}

function normalizeNameTokens(name: string | null | undefined): Set<string> {
  if (!name) return new Set();
  const cleaned = name.toLowerCase().replace(/[^a-zA-Z\s\-]/g, '');
  const tokens = cleaned.replace(/-/g, ' ').split(/\s+/).filter((t) => t.length > 1);
  return new Set(tokens);
}

export function validateCrossDocuments(
  contractData: Record<string, any>,
  nationalIdData: Record<string, any>,
  medicalData: Record<string, any>
): ValidationAlert[] {
  const alerts: ValidationAlert[] = [];
  const cCnp = (contractData.national_id || '').trim();
  const idCnp = (nationalIdData.national_id || '').trim();

  // 1. CNP Discrepancy & Checksum
  if (idCnp) {
    const { isValid, reason } = validateRomanianCnp(idCnp);
    if (!isValid) {
      alerts.push({ severity: 'critical', field: 'national_id', message: `National ID Card: ${reason}` });
    }
  }

  if (cCnp && idCnp && cCnp !== idCnp) {
    alerts.push({
      severity: 'critical',
      field: 'national_id',
      message: `CRITICAL DISCREPANCY: CNP on Contract ('${cCnp}') does NOT match National ID ('${idCnp}').`,
    });
  }

  // 2. Name Consistency
  const cTokens = normalizeNameTokens(`${contractData.first_name || ''} ${contractData.last_name || ''}`);
  const idTokens = normalizeNameTokens(`${nationalIdData.first_name || ''} ${nationalIdData.last_name || ''}`);

  if (cTokens.size > 0 && idTokens.size > 0) {
    const intersection = [...cTokens].filter((x) => idTokens.has(x));
    if (intersection.length === 0) {
      alerts.push({
        severity: 'critical',
        field: 'name',
        message: `Name mismatch: Contract name does not match National ID.`,
      });
    } else if (cTokens.size !== idTokens.size) {
      alerts.push({
        severity: 'warning',
        field: 'name',
        message: 'Minor name variation detected between Contract and National ID (e.g., omitted middle name).',
      });
    }
  }

  // 3. Medical Clearance Gatekeeper
  if (medicalData.medical_clearance_status === false) {
    alerts.push({
      severity: 'critical',
      field: 'medical_clearance',
      message: 'COMPLIANCE GATE: Medical certificate indicates candidate is UNFIT or unconfirmed.',
    });
  }

  // 4. Temporal Sanity
  if (medicalData.issue_date && contractData.start_date) {
    const examDate = new Date(medicalData.issue_date);
    const startDate = new Date(contractData.start_date);
    const diffDays = (startDate.getTime() - examDate.getTime()) / (1000 * 3600 * 24);

    if (diffDays > 180) {
      alerts.push({
        severity: 'warning',
        field: 'medical_clearance_date',
        message: `Medical clearance is older than 6 months prior to start date.`,
      });
    } else if (diffDays < -14) {
      alerts.push({
        severity: 'warning',
        field: 'medical_clearance_date',
        message: `Medical clearance date is set well after employment start date.`,
      });
    }
  }

  return alerts;
}

export function matchOption(value: string | null | undefined, options: readonly string[], fallback: string): string {
  if (!value || !value.trim()) return fallback;
  const clean = value.trim().toLowerCase();
  const matched = options.find((opt) => opt.toLowerCase().includes(clean) || clean.includes(opt.toLowerCase()));
  return matched || fallback;
}