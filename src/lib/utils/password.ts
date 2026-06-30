export function validatePasswordPolicy(pw: string, em: string = ""): string[] {
  const errors: string[] = [];
  if (pw.length < 8) errors.push("At least 8 characters");
  if (!/[A-Z]/.test(pw)) errors.push("One uppercase letter (A-Z)");
  if (!/[a-z]/.test(pw)) errors.push("One lowercase letter (a-z)");
  if (!/\d/.test(pw)) errors.push("One number (0-9)");
  if (!/[@#!%^&*()_+\-=\[\]{};':"\\|,.<>\/?~`]/.test(pw)) errors.push("One special character (@, #, !, %, &)");
  if (em && pw.toLowerCase() === em.toLowerCase()) errors.push("Cannot match email");
  return errors;
}
