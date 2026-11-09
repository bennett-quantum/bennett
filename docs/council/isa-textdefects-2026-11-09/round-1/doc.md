# Graded document: ISA 0.9 text-defect closures u94 (native-model/1 closed productions) + rqn (K85 numerical/channel domain and preparation evidence encodings), bennett-isa-spec job/isa-textdefects-u94-rqn b08940d, base isa-spec main 695cb4b

Determining defects (beads, verbatim titles): bennett-isa-spec-u94 and bennett-isa-spec-rqn; see the rationale below. Reference interpreter = oracle where text is silent (COMMON rule 1). Prior review round (not council): sol REVISE (SOL-TEXT-01 Occurrence identity, SOL-TEXT-02 image order vs K85 replay), astra REVISE (F1 = SOL-TEXT-01, F2 realised preparation prefix); one fix round b08940d (merge of main 1f87360 first); both seats' collision probes now report no collision.

## Bead u94
◐ bennett-isa-spec-u94 [BUG] · K86 native-model/1 lacks closed encodings for Kraus/instrument and explicit control representations   [P1 · IN_PROGRESS]
Created by: tobiasosborne · Type: bug
Created: 2026-11-08 · Started: 2026-11-09 · Updated: 2026-11-09

DESCRIPTION

  Determining sentence: ISA 0.9 §8.3 requires native-model/1 Kraus/instrument 
  equivalence and explicit per-context control models, but publishes only the 
  data.matrix plus controlled_U JSON fragment, so a closed reference reader   
  and portable nonunitary/duplicated-Kraus vectors cannot choose interoperable
  bytes without inventing a contract. At a0b49a0 spec/Bennett-ISA-Spec-0.9.md 
  lines 2024-2038 require Kraus/instrument reduced-map equivalence and actual 
  controlled implementations; lines 2047-2056 name data/control_models and    
  explicit models but define no productions for Kraus, instruments,           
  environment or full-context matrices. Lines 2069-2073 mention optional      
  enclosure/unitarity certificates without their schema. Only lines 2098-2109 
  encode data.matrix and                                                      
  control_models:{kind:controlled_U,controls:c,disabled:identity}. Full-spec  
  rg for                                                                      
  kraus|instrument|control_models|parameter_bindings|operand_map|unitarity    
  certificate|enclosure certificate|native-model/1 confirms no other          
  representation encoding. Publish the exact versioned closed productions,    
  including Kraus logical basis/environment treatment, control-context        
  selection and optional certificate encodings; then implement complete       
  reference decoding and canonical vectors. Existing interpreter has no       
  native-model oracle to preserve for these encodings. Do not reject a        
  promised representation or invent keys to close b-isa-spec-0ib. The exact   
  rational prerequisite is independently implementable; full model            
  reader/vector completion remains blocked.                                   



BLOCKS
  ← ◐ b-isa-spec-0ib: Implement ISA 0.9 K86 checker-native-model and publish conformance vectors P1

COMMENTS
  2026-11-09 09:25 tobiasosborne
    
      Determining sentence: candidate contract draft is implemented at            
      95fd0e04fc5565aadf0ec732e7c08850881ef070 (preceded by 83eb0eb), branch      

## Bead rqn
◐ bennett-isa-spec-rqn [BUG] · K85 conditional numerical/channel domain and preparation evidence encodings are unspecified   [P1 · IN_PROGRESS]
Created by: tobiasosborne · Type: bug
Created: 2026-11-08 · Started: 2026-11-09 · Updated: 2026-11-09

DESCRIPTION

  Determining sentence: ISA 0.9 K85 requires conditional numerical/channel    
  checks and checked image preparation, but its published closed certificate  
  payloads do not encode those inputs. Pinned spec/Bennett-ISA-Spec-0.9.md    
  lines 4080-4089 say apply the interval Frobenius procedure to (U-V)J_I and  
  use reduced-input/full-output Choi maps; the numerical/channel payload table
  in section 12.1 has no domain or image field. Lines 4397-4405 require       
  checked preparation/binding, exact classical bytes, entry factorisation and 
  exit restoration, while section 12.3 certificate/launch bindings contain no 
  preparation witness field. Standing rule 1: retain existing reference-      
  interpreter Unverified interval/target checks and conditional-only theorem  
  behaviour; do not invent an admitted producer assertion or silently         
  discharge invocation applicability. Publish explicit versioned              
  domain/preparation encodings and binding/reuse rules, then implement the    
  rigorous checker and native launch attachment. Found during b-isa-spec-qrc  
  implementation at baseline 62a0cf0.                                         



NOTES

  Pinned 62a0cf0 exact text locations: spec/Bennett-ISA-Spec-0.9.md lines     
  3839-3840 (numerical/channel payload table) contain subject, metric,        
  precision_bits, bound, and channel dual, but no domain/fixed_regions field. 
  Line 4089 says: "For conditional numerical claims, apply the interval       
  Frobenius-bound procedure to (U−V)J_I. For conditional channel claims, form 
  the Choi matrix of (E_real−E_ref) composed with Ad_J_I, using the reduced   
  input dimension and complete output dimension; retain the existing rigorous 
  interval and invocation-context checks."                                    
                                                                              
  Lines 4397-4405 say: "A proof_relative_to_image theorem is conditional on   
  the stated image." Using it requires "checked preparation/binding           
  establishing that this in-region contains exactly those classical bytes and 
  is factorised from other systems at entry, and that its exit image is       
  restored." No closed certificate/launch payload specifies that witness or   

## Diff of spec/ (695cb4b..b08940d)
```diff
diff --git a/spec/Bennett-ISA-Spec-0.9.md b/spec/Bennett-ISA-Spec-0.9.md
index bda5b1a..dac7fd8 100644
--- a/spec/Bennett-ISA-Spec-0.9.md
+++ b/spec/Bennett-ISA-Spec-0.9.md
@@ -2129,6 +2129,182 @@ At c=1 the model reconstructs diag(I2,X); adding model bytes changes target_hash
 
 Closed-schema target readers MUST be upgraded for realisation_model; missing or unsupported models follow the reporting rules above and MUST NOT be silently substituted by ideal operations.
 
+**Closed native-model/1 productions.**
+
+The following productions complete the version named above. A model producer
+MUST emit UTF-8 JCS, without a trailing LF in hashed bytes, using exactly the
+fields of the selected production; a model reader MUST reject duplicate,
+unknown or missing fields, wrong types and malformed data in a recognized
+version. Readers dispatch on version before checking that version's fields;
+an unknown version receives unsupported-model reporting, not guessed decoding.
+`?` means optional, `...` means repetition, and alternatives below are
+discriminated by their printed fields, never by a guessed matrix dimension.
+Object field order is JCS order; array order is significant. A `uint` is a
+nonnegative integer, encoded as a JSON number below 2^53 and otherwise a
+canonical unsigned decimal string (§9.1); a positive integer excludes zero.
+A `label` is a nonempty ASCII string. A `hash` is 64 lowercase hexadecimal
+digits. No numerical string has whitespace, a leading `+` or a leading zero
+except the single digit `0`; negative zero is not a rational spelling.
+
+```text
+Model = {"version":"bennett.native-model/1","kind":"unitary",
+         "arity":Size,"basis":Basis,"parameter_bindings":Bindings,
+         "operand_map":Map,"control_models":Control,"data":Data}
+Bindings = { <label>: "k" | "c" | "eps" | "theta", ... }
+Control = {"kind":"controlled_U","controls":"c","disabled":"identity"}
+        | {"kind":"explicit","controls":"c"}
+Data (controlled_U) = Operation
+Data (explicit) = {"contexts":[
+  {"controls":{"min":uint,"max":uint|"unbounded"},"data":Operation}, ...]}
+Operation = {"matrix":Mat,"representation"?:Representation,
+             "certificates"?:Certificates}
+Representation = {"kind":"kraus","operators":[Mat, ...]}
+               | {"kind":"instrument","outcomes":[
+                   {"label":label,"operators":[Mat, ...]}, ...]}
+               | {"kind":"environment","arity":Size,
+                  "state":Mat,"matrix":Mat}
+Basis = [label, ...] | {"controls":"c","targets":[label, ...]}
+Map = [uint, ...] | {"kind":"entry_to_allocation"}
+Size = uint | {"var":"k"|"c"}
+     | {"op":"+"|"-"|"*","args":[Size,Size]}
+     | {"op":"pow2","args":[Size]}
+Rat = ["<signed numerator>","<positive denominator>"]
+Expr = Rat | {"var":label}
+     | {"op":"pi"|"i","args":[]}
+     | {"op":"+"|"-"|"*"|"/","args":[Expr,Expr]}
+     | {"op":"sqrt"|"exp"|"sin"|"cos","args":[Expr]}
+Complex = [Expr,Expr]
+Mat = [[Complex, ...], ...]
+    | {"kind":"identity","dimension":Size}
+    | {"kind":"zero","rows":Size,"columns":Size}
+    | {"kind":"diagonal","entries":[Complex, ...]}
+    | {"kind":"adjoint","matrix":Mat}
+    | {"kind":"scale","scalar":Complex,"matrix":Mat}
+    | {"kind":"sum"|"product"|"tensor"|"block_diagonal",
+       "matrices":[Mat, ...]}
+    | {"kind":"controlled","controls":Size,"matrix":Mat}
+    | {"kind":"tensor_power","count":Size,"matrix":Mat}
+Certificates = {"unitarity"?:
+  {"version":"bennett.unitarity/1","gram":Mat},
+  "enclosure"?:{"version":"bennett.enclosure/1","precision_bits":uint,
+                "matrix":[[[Rat,Rat,Rat,Rat], ...], ...]}}
+```
+
+All lists printed with `...` may be empty only where their meaning below
+permits it. The reader MUST validate expression nodes and dimensions before
+using a model: rational leaves are reduced with strictly positive denominator
+and zero exactly `["0","1"]`; every expression is finite; divisions by zero,
+unbound variables and negative Size results reject. `Expr` has the ordinary
+complex analytic meanings, using the principal complex square root (on the
+negative real axis its imaginary part is positive). `[a,b]` denotes a + i b,
+including when either expression is complex. Bindings may alias the four
+resolved sources, but a key named k, c, eps or theta retains that same source.
+Only declared aliases occur in Expr; Size uses the resolved k and c directly.
+An unavailable source rejects that context. In particular eps is available
+only at positive achieved epsilon, theta only for a parametric opcode and as
+the exact finite binary64 rational; k and c always retain §8.1's meanings.
+
+Dense matrices have at least one row and column and equal row lengths.
+Rows index outputs and columns inputs. Matrix constructors have their usual
+linear-algebra meanings: sum/product lists are nonempty, sums have equal
+shapes, products multiply left to right and adjacent dimensions agree;
+tensor/block_diagonal lists are nonempty and preserve list order. Identity
+and zero dimensions are positive. A diagonal list is nonempty. Controlled
+has a square matrix M and denotes diag(I,...,I,M), with 2^controls blocks;
+tensor_power repeats its matrix in tensor order, with count zero denoting
+the 1-by-1 identity. The checker MUST reject incompatible shapes rather than
+pad, truncate or transpose matrices. These constructors permit symbolic
+generation without a materialised-dimensional cap; they do not add cost
+expression operators to §8.1.
+
+For controlled_U, arity is the opcode's target count (one, or two for
+swap/cz); basis is an array containing exactly t, or exactly t and t2, in
+any order. For explicit, arity is c plus that target count; basis lists
+each c[0] through c[c-1] and every target exactly once. The template Basis
+expands to c[0],...,c[c-1] followed by its targets array and is available
+only in explicit form. Size and Basis are resolved anew at each context.
+The model reader MUST reject any arity/basis disagreement or non-permutation
+operand_map. Matrix basis bit 0 is the first listed bit and is the
+most-significant bit of a row/column index. This orders individual wires;
+the bits within a source bundle are still enumerated least-significant first.
+
+For controlled_U the complete model order is the entry's own controls,
+then effective controls, then the listed base basis. For explicit it is
+the expanded full basis; c[j] names the same §8.3 entry-order control j.
+operand_map maps each bit of this complete order to its allocation-order
+position among these operands, with inherited controls first. The generated
+entry_to_allocation Map denotes exactly this permutation, derived from
+resolved operand identities, including target-basis permutations. The checker
+MUST compare a supplied permutation to those identities and apply it to both
+row and column indices of every logical matrix, never to environment bits.
+
+In explicit form the contexts list is nonempty, sorted by increasing min,
+with disjoint inclusive ranges and max >= min. The reader MUST select exactly
+one row for each admitted resolved c and reject a missing or overlapping
+selection; an unbounded range is last. The row's expressions may depend on
+all its declared bindings, including k and theta. Its Operation describes
+the actual full context, including disabled branches and relative phase;
+it is not controlled again. In controlled_U form, each Operation describes
+the base operation and the target author binds diag(I,...,I,U) as the actual
+implementation, with no independent per-Kraus control construction. These
+rules apply to every admitted context, including c=0 and zero epsilon.
+
+In either form `matrix` supplies the phase-bearing U of the represented
+logical dimension. An omitted representation denotes precisely Ad_U.
+Kraus operators are a nonempty ordered list of square matrices on that same
+logical basis. Their map is sum_a K_a rho K_a†; no extra environment input
+is inferred. Instrument outcomes are a nonempty list with distinct labels
+in bytewise order and nonempty ordered Kraus lists per outcome. Their
+classical outcome is discarded in the reduced logical map; neither an
+outcome nor a Kraus index becomes a logical wire or a coherent control.
+Permutation of a Kraus list changes bytes, even when it preserves the map.
+
+An environment representation has e=arity environment qubits, basis e[0]
+through e[e-1] in that order, and an exact density matrix state of size 2^e.
+Its matrix W acts on logical bits first, then environment bits; both factors
+use the most-significant-first convention. The environment is initially
+factorised from every logical/external system. The checker MUST check state
+Hermitian positive semidefinite with trace 1, W†W=I, and the map
+Tr_env(W(rho tensor state)W†); e=0 is legal and has state [[1]] in mathematical
+notation, encoded with the same Complex/Rat productions. Environment
+outputs are traced, never omitted logical outputs. A mixed state is allowed;
+no assumption of a pure zero environment is implicit.
+
+For either Kraus or instrument representation the checker MUST check
+sum_a K_a†K_a=I, then, for every pair of logical basis indices i,j, check
+that its reduced map on the matrix units |i><j| equals U|i><j|U†. The same
+matrix-unit equivalence applies to an environment representation. All these
+checks include off-diagonal units and arbitrary external references by
+linearity. The checker MUST separately establish U†U=I and the existing
+phase-sensitive native epsilon obligation; a valid CPTP representation
+does not prove either one. With controlled_U these representation checks
+are base checks plus the explicit actual-controlled-unitary binding, while
+explicit rows check their full-context representation directly.
+
+Optional certificates assert facts about this Operation's U, not a substitute
+operation. The enclosure matrix has U's dense shape; an entry
+[re_lo,re_hi,im_lo,im_hi] uses exact reduced rational endpoints with ordered
+closed intervals. precision_bits is positive. The checker MUST independently
+enclose each exact U entry using §12.1's outward interval arithmetic at that
+precision and verify containment in the supplied box; a disjoint or
+inconclusive containment check does not pass. The unitarity certificate's
+gram has U's shape. The checker MUST establish exactly both gram=U†U and
+gram=I, not merely that each interval contains the identity. No enclosure
+width, claimed Gram matrix or producer success flag establishes an exact
+identity. Exact rational evaluation or a checked symbolic equality may
+discharge it; unsupported exact identities remain unchecked. Certificate
+fields, matrices and expression trees are hashed as part of the target.
+
+For a well-formed but unimplemented representation, constructor or certificate
+version, the checker MUST report the affected obligation unchecked with an
+unsupported-model diagnostic, never silently ignore supplied data or compare
+the ideal opcode to itself. A malformed known production or a refuted
+obligation rejects. An unresolved symbolic identity or host checking limit
+retains the existing unchecked outcome and discharges no executable claim.
+These are checking outcomes, not restrictions on source programs or admitted
+algorithm dimensions. All previous zero/positive-epsilon compatibility and
+target/schedule/source identity rules above remain in force.
+
 ### 8.4 Space budget
 
 The capacity constraint is peak live qubits per class.
@@ -3956,8 +4132,8 @@ Witness envelope SHA-256: `299510fd67cc626fdcbcc10adcd40730f9af294ba596d86fb25fd
 | `exhaustive` | `domain` (§12.2); `expected`: `"oracle"` \| `{ "table": [...] }` \| `{ "program": closure_hash }` \| `"inverse_pair"` | re-execute every domain element on the reference interpreter / expected program; compare full tuples. For `"inverse_pair"` (the claim of an `inverse_pairs` entry, §12.3): for every element (x, ins, mem cells, args) run g and ginv at the entry's tuple, token-typed arguments at their `arg_tokens` tuples, and require both fault-free, ginv(g(x)) = x and g(ginv(x)) = x; the bundles and regions components MUST be the full domain of g's `in` and `mem` slots (the `args` component lists the covered classical values) |
 | `sampled` | `domain`; `expected`: `"oracle"` \| `{ "table": [...] }` \| `{ "program": closure_hash }`; `subject` and invocation binding as below (K13); `sampler`: `{ "algorithm": "xoshiro256**", "seed": [4 decimal strings, not all zero], "count": n }` | independently replay both sides of the declared relation on every sampled element; compare full tuples; always **evidence**, even if every element is drawn |
 | `structural` | `{ "rule": "translation_lemma" \| "inverse_pair_library" \| "adjoint_table", "subclaims": [indices], "witness": … }`; for `translation_lemma`: `{ "V": [points], "W": [points], "X": [wires], "B": [wires], "frame": [first point, last point] }`; for `inverse_pair_library`: `{ "library_closure_hash", "claim_index" }`; for `adjoint_table`: `{}` | check the rule's side conditions syntactically against the object and the subclaims' results |
-| `numerical` | `{ "subject": { "closure_hash", "variant", "inherited_controls", "schedule_hash" }, "metric": "operator_norm", "precision_bits": n, "bound": decimal }` | **checker-computed, for every invocation context of the subject** (below): build the realised unitary U of that invocation (the region's realisation under the root schedule at that path, with its resolved classical arguments, budget, epsilon shares and cleanup choices, and `inherited_controls` control wires prepended) and the reference unitary V (the region's §5.3 semantics with the same arguments, controlled on the same wires) at the subject's signature widths in interval arithmetic at `precision_bits` (basis order = allocation order, controls first), form interval enclosures of `V†U − I` entrywise, derive the operator-norm bound as the Frobenius-norm upper bound in interval arithmetic, and verify it is ≤ `bound`; the claim holds iff it holds for every context |
-| `channel` | `{ "subject": as above, "metric": "diamond", "precision_bits", "bound", "dual": [ { "Y": interval Hermitian matrix, "mu": decimal } … ] }` | for every invocation context of the subject, in enumeration order, verify its dual witness for the **diamond-norm SDP** below in interval arithmetic and `mu` ≤ `bound` (one witness per context; too few witnesses: reject) |
+| `numerical` | `{ "subject": { "closure_hash", "variant", "inherited_controls", "schedule_hash" }, "metric": "operator_norm", "precision_bits": n, "bound": decimal, "domain"?: { "version": "bennett.process-domain/1", "fixed_regions": [ { "name", "A", "W", "image", "sha256" } … ] } }`; domain production/binding: §12.3 | **checker-computed, for every invocation context of the subject** (below): the checker MUST build the realised unitary U and reference unitary V at that context's resolved arguments, budget, shares, cleanup choices and inherited controls, in allocation basis, controls first; with absent/empty fixed_regions, enclose `V†U − I`, otherwise enclose `(U−V)J_I` with the reduced input and complete output (§12.3); compute the interval Frobenius upper bound at positive `precision_bits` and verify it is ≤ the nonnegative finite `bound`. The checker MUST report a bound only if every context passes, retaining its full-domain or conditional-image scope and separate preparation applicability; inconclusive interval checks do not pass |
+| `channel` | `{ "subject": as above, "metric": "diamond", "precision_bits": n, "bound": decimal, "domain"?: { "version": "bennett.process-domain/1", "fixed_regions": [ { "name", "A", "W", "image", "sha256" } … ] }, "dual": [ { "Y": interval Hermitian matrix, "mu": decimal } … ] }`; domain production/binding: §12.3 | the checker MUST verify exactly one dual witness per invocation context in enumeration order (too few or too many reject), for the **diamond-norm SDP** below applied to `(E_real−E_ref) ∘ Ad_J_I` when fixed_regions is nonempty and to the unrestricted maps otherwise. Y has dimension `(d_in*d_out)` square, with reduced d_in and complete d_out for an image; the last SDP matrix has dimension d_in and traces d_out. The checker MUST apply the existing strict interval-pivot procedure at positive `precision_bits`, check nonnegative finite mu ≤ nonnegative finite `bound`, and report only the scope actually checked; a process bound does not itself establish image preparation or exact exit restoration (§12.3) |
 
 **Adjoint-table side conditions (K94).** A `structural` claim with
 `rule:"adjoint_table"` asserts that the §5.3 adjoint construction of its
@@ -4589,7 +4765,7 @@ an action region[63,1] with `cells: "all"` and `count: 1` remains legal but has
 ### 12.3 Schema and composition
 
 ```
-  versions; bindings { object_hash, interface_hash, closure_hash (required), reference_program_hash, dialect_mapping_version, target_hash, schedule_hash?, invocation? (K13) }
+  versions; bindings { object_hash, interface_hash, closure_hash (required), reference_program_hash, dialect_mapping_version, target_hash, schedule_hash?, invocation? (K13), preparation? (K85) }
   producer { name, version, materialisation { llvm_version, pipeline, normaliser_version } }
   regions { <closure_hash>: { kind, signature, bounds, estimate? (K12), frame?: <§9.4 descriptor>, frame_contexts?: [{context_key:<§12.1 key>, frame:<§9.4 descriptor>}], resources { encoded_row_name: canonical_decimal_string }, resource_contexts?:[{context_key,resources,gates_used,estimate?}], gates_used { gate: { count, scheme?, epsilon? } },
             claims: [ <claim> … ], verification: { oracle: i, borrow_frames: [i], inverse_pairs: [ { g, ginv, claim: i, budget: [B,heap,stack,depth], arg_tokens?: { "<arg>": [B,heap,stack,depth] } } ], unitary: [i], channel: [i],
@@ -4639,6 +4815,279 @@ configuration are recorded as required by the North Star.
 
 VM objects contain the selected marked entries and their required transitive device closures. Code outside those closures remains native; shared callees may have both host and device variants. Native comparison uses the materialised entry and its entire materialised callee closure with the North Star §3.2 runtimes and arithmetic libraries.
 
+**Process-domain and preparation bindings (K85).**
+
+The optional numerical/channel `domain` is the closed
+`bennett.process-domain/1` production in §12.1's payload rows. Its
+fixed_regions entries use exactly §12.2's name, A, W, little-endian raw image
+and SHA-256 encodings, with nonnegative integer A and positive W under §9.1.
+The certificate producer MUST list them in interface mem-slot order and the
+checker MUST resolve and validate them against that subject, rejecting a
+duplicate, mut-role region, bad shape, nonzero padding or stale raw-byte hash.
+All components other than those fixed in-role cells remain unrestricted,
+including inherited controls, arbitrary initial target/fault, borrowed
+systems and all mut-role cells. No replay omission-at-zero rule applies to
+this process production. Absent domain and an explicit domain with an empty
+fixed_regions array both mean the full original D. Additional fields, including
+bundle slices, are malformed in this version, not ignored restrictions.
+An unsupported process-domain version leaves the claim Unverified; the reader
+never interprets it as an empty or unrestricted domain.
+
+For each context, remove the fixed cell bits from the ordered input basis;
+J_I inserts their declared basis values at those same positions, together
+with the prescribed workspace/local initialisations. Remaining input bits
+retain their relative allocation order. Output retains the complete output
+interface, borrowed systems and all workspace/local outputs required to
+observe their restoration; it does not project out the fixed cells or hide
+leakage. Let d_in be the dimension after insertion inputs are removed and
+d_out the complete output dimension. For channel witnesses the input-first
+Choi row index is i*d_out+a (input i, output a); columns use j*d_out+b.
+Tr_out(Y)[i,j] is sum_a Y[i*d_out+a,j*d_out+a]. For numerical claims use the
+rectangular `(U−V)J_I` before taking the Frobenius bound; multiplication by
+V† is only the unrestricted-unitary alternative already in §12.1. In the
+strict-feasibility padding recipe, the trace factor d is d_out and the
+slack identity is I_d_in. These rules encode reduced-input/complete-output
+claims without discarding coherent leakage, relative phase or external
+references.
+
+A successful fixed-image process bound is conditional on I and is reported
+as such with its metric, bound, subject, claim index and ordered resolved
+image bindings. It is neither an unrestricted bound nor an exact permutation
+proof. In particular a nonzero process-error bound does not prove exact image
+restoration. Where an executable use requires preparation, the checker MUST
+report its applicability separately as established or unestablished; without
+a checked attachment below the bound/theorem remains conditional. This also
+applies to §12.2's proof_relative_to_image. Existing reference-interpreter
+Unverified outcomes for unavailable target/interval checks remain Unverified;
+adding domain metadata or a preparation descriptor cannot upgrade them.
+
+The certificate binding extension and its closed records are:
+
+```text
+bindings.preparation = {"version":"bennett.image-preparation/1",
+                       "entries":[Attachment, ...]}
+Attachment = {"closure_hash":hash,"claim":uint,"context_key":ContextKey,
+              "invocation":Invocation,"images":[Image, ...],
+              "witness":Witness,"restoration":Restoration}
+Image = {"name":label,"A":uint,"W":uint,"image":hex,"sha256":hash}
+Witness = {"kind":"logical","regions":[
+  {"name":label,"allocation":Occurrence,"prepare":[Occurrence, ...]}, ...]}
+        | {"kind":"launch_copy","manifest_hash":hash,"copy_indices":[uint, ...]}
+Restoration = {"kind":"matrix_units"}
+            | {"kind":"claim","claim":uint}
+Occurrence = {"context_key":ContextKey,"symbol":hash,"point":string,
+              "iteration":[uint, ...],"instance":[uint, ...],
+              "step"?:uint,"phase"?:"fwd"|"rev","generated":uint,
+              "allocation"?:Allocation}
+Allocation = {"context_key":ContextKey,"symbol":hash,"point":string,
+              "iteration":[uint, ...],"instance":[uint, ...],
+              "step"?:uint,"phase"?:"fwd"|"rev","generated":uint}
+```
+
+Preparation descriptors and the launch manifest below are UTF-8 JCS with
+exactly the selected production's fields and significant array order;
+duplicate/unknown/missing fields, noncanonical bytes and wrong types are
+malformed for a recognized version. Version dispatch precedes field decoding.
+An absent bindings.preparation or empty entries array supplies no attachment.
+
+Here hash/uint have §8.3's canonical encodings; `hex` is lowercase raw-byte
+hex with exactly the length and padding of §12.2. `label` in Image/regions
+is the subject's interface-region local name (the existing NAME repertoire,
+not §8.3's ASCII-only model labels). ContextKey is the complete §12.1 key,
+relative to this certificate's root, with [] for that root. Invocation is
+the concrete §12.3 args/budget/token_aliases record, never its `"all"` form.
+An Occurrence identifies one concrete public expansion leaf in the invocation
+denoted by context_key. Its symbol is the defining source function's §9.2
+interface hash (including an inlined lproc's own hash); point is that function's
+§11 source point, including nested-body components, or its permitted reserved
+pseudo-point. iteration is the complete vector of enclosing source-qloop
+repetition counts, outermost first; instance is the §3.7 fixed-binding integer
+key, [] outside an lproc instance. Both arrays are present, including when
+empty. The terminal coordinates are independent of those on context_key's
+call edges; lift.call adds no edge. step and phase are both present exactly
+when this terminal leaf has a containing oracle step under §11, with step in
+1..that invocation's B and phase fwd or rev. Both are absent at a level with
+no step, including action support and oracle construction/commit/release;
+outer call-edge step/phase coordinates remain in context_key.
+
+generated is the leaf's public §11 bound-library ordinal at that terminal
+point and coordinates, before target-scheme expansion, not a private checker
+instruction number. A source instruction selects a leaf of its expansion
+only with that ordinal; it never denotes all visits or all leaves at once.
+A realised claim uses its root schedule's bindings.expansion; a reference-only
+claim uses §17 item 7's default ref library for this ISA version. Missing
+expansion/checking mechanics leave applicability unestablished.
+
+Allocation encodes the same coordinates of the leaf acquiring the allocation
+in the forward expanded construction. It has no recursive allocation field.
+This forward acquisition address identifies the allocation lifetime, rather
+than a storage address, declaration name or subject interface name; different
+acquisitions of one declaration have distinct addresses. For every K83
+action-local region support leaf, allocation is required and equals the
+forward acquisition address of that declaration's region storage. Thus all
+allocation, image-preparation, restoration and release leaves for one such
+region carry the same forward acquisition address, while generated still
+distinguishes individual leaves. For these pseudo-points iteration and instance
+are [], and step/phase are absent, as §11 K83 prescribes. Outside K83 support,
+allocation is absent; an allocation occurrence's own complete leaf address
+identifies its lifetime, and operand/lifetime mappings resolve other leaves.
+Raw reversal retains the forward points, ordinals and allocation identities
+under K63/K64/K83; inverse oracle step t has (step:t, phase:rev) under
+§11, distinct from its forward step. Raw inversion of an already expanded
+trace retains that trace's leaf coordinates while adjointing its operations.
+Source adjoints instead use the source-adjoint construction's own §11 addresses.
+
+The certificate reader MUST validate every Occurrence and Allocation against
+the linked construction, rejecting wildcard selectors, missing or stale
+coordinates, a wrong ordinal/allocation identity and any address that does
+not resolve to exactly one leaf and the required allocation lifetime. These
+are public source/expansion coordinates, never a host PC or process-local id.
+Attachment.claim indexes the named closure's claims array in this certificate.
+Attachments
+are sorted by closure_hash, then claim numerically, then JCS context_key
+bytewise, with no duplicate triple. Images and logical regions are nonempty
+and in subject interface mem-slot order. Preparation occurrences are in actual
+semantic execution order, with duplicate detection on the complete resolved
+leaf address (including terminal coordinates and generated), not point alone.
+An inconsistent allocation field rejects rather than creating another leaf.
+A logical witness's regions list contains exactly one entry for each attachment image, with no
+other region; copy_indices likewise has exactly one index per image.
+
+The certificate reader MUST reject malformed known-version records and
+attachments whose claim, images, invocation or context conflict with their
+resolved subject. Resolve both images and the claim's fixed_regions to
+subject mem-slot identities and compare their complete bindings (identity,
+A, W, raw image bytes and sha256) after canonical ordering by mem slot.
+Equality is independent of the replay claim's original fixed_regions array
+order; Attachment.images remains in canonical mem-slot order. No missing,
+extra, duplicate or unequal binding is accepted. This does not reorder or
+rewrite existing §12.2 replay claims or change their accepted bytes.
+The attachment's invocation equals the independently resolved nested args,
+budget and token_aliases, not the root's values copied into a callee.
+For reference-only claims the context tree is the bound reference Q
+construction; for realised claims it is §12.1's complete scheduled tree,
+including default-covered and coherently disabled calls. Each executable
+use requires its own attachment for every applicable context. An attachment
+for another device root, claim index, image, variant/control count or context
+does not establish this use. No process-local handle is serialized.
+
+For a logical witness, the checker MUST resolve every listed allocation
+and preparation occurrence to the actual linked logical program, prove that
+the allocated cells begin in the prescribed clean zero factor, and reconstruct
+the declared classical image from those operations, including any literal
+image initialisation prescribed by the allocation itself. It then tracks the
+allocation and call-operand mappings to the subject's in-role mem slot at the
+selected invocation's entry. It checks the complete intervening operation
+sequence, including operations not listed in prepare, to establish the exact
+image and factorisation from every other system at entry. A producer's
+occurrence list is a selection aid, not permission to omit interfering
+operations or coherent alternatives. A checked general logical preparation is
+permitted; zero allocation followed by X on precisely the set image bits is
+the basic case. Unknown coherent data is never inspected, measured, cloned
+or assumed zero to establish preparation.
+
+For executable applicability, the checker MUST reconstruct the preparation
+and every intervening operation of the realised prefix from the bound root
+schedule, resolved invocation contexts and actual target realisation models,
+including selected schemes, cleanup choices, shares, default-covered operations
+and coherent control branches, and prove the exact required entry image and
+factorisation on the covered root input domain with arbitrary external
+references. A reference/logical preparation proof can supply this premise
+only after checking that the realised prefix has the same required image and
+factorisation; a source-only preparation proof never establishes a different
+realised prefix. Merely binding a schedule hash or checking restoration on the
+conditional callee image does not prove entry. Missing realisation mechanics
+leave executable applicability unestablished while retaining an independently
+proved conditional theorem. A positive advertised epsilon does not preclude
+an exact image/factorisation proof for the realised prefix; no blanket
+zero-epsilon preparation restriction applies.
+
+For a launch_copy witness the named manifest has this closed JCS production:
+
+```text
+ImageLaunch = {"version":"bennett.image-launch/1",
+  "bindings":{"object_hash":hash,"interface_hash":hash,"closure_hash":hash,
+              "target_hash":hash,"schedule_hash":hash,"invocation":Invocation},
+  "copies":[{"context_key":ContextKey,"mem_slot":uint,"A":uint,"W":uint,
+             "image":hex,"sha256":hash}, ...]}
+```
+
+The manifest hash is SHA-256 of its exact UTF-8 JCS bytes without LF.
+copies are ordered by JCS context_key bytewise then mem_slot numerically,
+with no duplicate pair; mem_slot is the subject's signature mem position.
+copy_indices select, in attachment image order, exactly the matching copies.
+The manifest binds the actual selected device object/root and its root
+invocation; each copy's context resolves that invocation's reached callee,
+never the native host's main or an unrelated marked object. A launch manifest
+may supply several attachments; every use validates its own context/mem slot.
+
+The launch provider MUST independently validate the manifest bindings and
+raw-byte hashes, allocate or establish a fresh clean device factor, and
+perform the declared logical preparation/copy from those classical bytes
+before the selected invocation, with that image factorised from all other
+systems. It binds the resulting in-region and its
+actual opaque handle to this use internally, preserving packing, shape and
+factorisation until entry, without admitting a producer boolean as evidence.
+The provider MUST prevent concurrent mutation/rebinding through completion
+of that invocation; a changed image, mapping, handle lifetime or intervening
+operation invalidates the attachment. An existing unknown coherent region
+cannot be made applicable merely by asserting a matching hash. Native
+database construction/snapshot bytes are allowed; host pointer identity or
+a hash of an unobserved device state is not a preparation witness.
+
+This manifest specifies logical by-value image attachment, not a new C
+entry point, host-memory-by-reference layout or container ABI. The mixed
+boundary contract above still supplies actual root/handle ownership and
+transport. A deployment unable to associate and check this attachment
+reports applicability unestablished; it neither invents an ABI nor rejects
+an otherwise legal program. A static checker alone can validate the template
+but cannot attest that a future launch actually performed the copy. The
+launch provider's checked runtime association is additionally required.
+
+For either witness the checker MUST independently check exact exit restoration
+and factorisation of each fixed in-region. `matrix_units` directs reconstruction
+of the actual map on all matrix units of the remaining input (with arbitrary
+external references), checking that its complete output is supported on the
+same fixed image tensor the other outputs. For a unitary this can equivalently
+check zero amplitude outside that image. A restoration claim names an earlier
+claim in the same closure's claims array, with the same subject, context,
+invocation and image; the checker validates that its established exact full-tuple
+relation proves this restoration. A sampled, approximate, unrelated or
+unverified claim does not suffice. An exhaustive exact permutation relation
+can establish restoration by its full-tuple checks and linearity; a basis
+table cannot establish it for a non-permutation implementation. No circular
+preparation/restoration dependency is allowed. A reference-only theorem
+does not establish restoration of a different realised map.
+
+Readers and checkers MUST report unsupported descriptor versions or unavailable
+preparation/restoration mechanics as unestablished applicability, retaining
+any independently proved conditional theorem; malformed bindings and refuted
+preparation/restoration reject the attachment. The executor MUST use a
+conditional result to discharge an invocation only after matching all object,
+closure, target, schedule, claim/domain, variant/control, concrete invocation
+and context bindings and checking both entry and exit obligations. Reuse of
+the conditional theorem for identical immutable bindings is allowed; each
+actual launch still needs checked fresh preparation/association. Retaining
+only a raw image hash or copying an old attachment to a new handle is
+insufficient. Absence of applicability never turns a conditional bound into
+an unrestricted proof or discharges a full-D borrow-frame/inverse obligation.
+
+The composition checker MUST establish the required image/preparation and
+restoration bindings at every callee use before including a conditional bound
+in local/inclusive error or multiplicity composition. It propagates mem-slot
+identities through actual call operands and verifies the relevant entry images;
+one callee's conditional bound cannot cover an unrelated image or another
+context by sharing a closure hash. Missing applicability leaves that composed
+obligation unestablished, even if every isolated conditional claim passed.
+
+Producers and readers MUST include the new domain/preparation bytes in the
+ordinary certificate hash/cache identity. Manifest bytes have their own hash
+as above; a changed manifest requires a changed attachment/hash. These additions
+do not alter source/interface/closure/object identities or target/schedule
+hashes when those artifacts' bytes are unchanged. Regenerated targets,
+schedules, source or headers follow their existing identity rules. The
+descriptors do not waive target/error/resource composition obligations.
+
 **Native-model mixed-object binding (K86; §§9–10).**
 
 A mixed binary's native host runs main, argv/envp,
@@ -5221,6 +5670,143 @@ The vectors record source admission, complete output tuples and expanded source
    libc need no fabricated device alias entries. A native layout version
    alone cannot authorize an alias-aware launch/sched request.
 
+**Native representation conformance (K86; suites D/F).**
+
+1. **Closed bytes and exact expressions (producer/reader).** Round-trip the
+   existing X fragment completed with operand_map [0], then its negative-X
+   variant. Exercise every dense/generated matrix constructor, zero
+   tensor_power, canonical integer boundaries, reduced rational zero and
+   positive denominator, binary64 theta=0.1 and negative zero. Observe exact
+   context values (theta=3602879701896397/36028797018963968 for 0.1), not a
+   decimal approximation. Unknown/duplicate fields, wrong node arity,
+   undeclared variables, zero divisors, ragged matrices and wrong dimensions
+   reject; legal unmaterialisable dimensions report unchecked host limits.
+2. **Kraus and instruments (checker).** With U=X, two duplicated Kraus
+   operators X/sqrt(2) establish Ad_X; the one-outcome instrument containing
+   them and the two-outcome instrument with one each have the same reduced
+   map. X/sqrt(2), ZX/sqrt(2) are CPTP but send |+><+| to I/2, so reject
+   equivalence to U=X. Include all off-diagonal matrix units, non-TP sums,
+   empty lists, duplicate/unsorted outcome labels and phase-bearing U omitted.
+   Neither a Kraus index nor an outcome adds a logical input.
+3. **Environment (checker).** e=1, state=|0><0| and W=X tensor I reduce to
+   Ad_X; the mixed state I/2 gives the same result. W=SWAP with that zero
+   environment resets a logical input and rejects equivalence to X. Reject
+   a negative eigenvalue in state, nonunit trace, a nonunitary W and swapped
+   tensor factors; include e=0 and an entangled external reference. Observe
+   no environmental output being mistaken for a discarded logical output.
+4. **Explicit controls (reader/checker).** Compare controlled_U X at c=0,1,2
+   with explicit context rows for those counts, and a generated unbounded
+   full-context rule. At c=1 diag(I2,X) passes zero epsilon; diag(I2,-X)
+   has operator error 2 and rejects epsilon 0 or 1, accepting 2 when the
+   requested share permits it. Identity-disabled and phase-sensitive checks
+   use full context matrices, irrespective of equal uncontrolled channels.
+   Missing/overlapping contexts, wrong selected k/theta and double-control
+   reconstruction reject.
+5. **Basis and permutation (checker).** For cx with own control a and
+   inherited q, entry order [a,q,t] maps to [q,a,t] by [1,0,2]; compare its
+   explicit c[0],c[1],t matrix with the base controlled_U model. Reverse
+   t,t2 in a two-target base and transform both rows and columns. Reject a
+   stale map, repeated/missing bit, swapped inherited control or environment
+   bit in operand_map; generated entry_to_allocation agrees with the explicit
+   identity-derived permutation.
+6. **Optional certificates (checker).** Accept exact Gram I for X only after
+   recomputing X†X. Substituting 2X with the same claimed Gram rejects.
+   Enclose X with degenerate rational boxes and a transcendental rotation
+   with independently computed outward boxes. An endpoint outside the box,
+   reversed endpoints, zero precision or wrong shape rejects; an inconclusive
+   enclosure or exact identity never passes. A box containing I does not
+   prove unitarity. Exercise unsupported certificate versions explicitly.
+7. **Compatibility and identity (producer/reader/checker).** Missing positive
+   epsilon models, unsupported versions/representations/constructors and
+   unresolved exact identities leave the affected obligations unchecked,
+   with no ideal self-comparison. Missing zero-epsilon models retain the
+   exact-opcode convention; contradictory supplied models reject. Changing
+   representations, Kraus order, certificates or context rows
+   changes target_hash and dependent schedule_hash, while fixed source/header
+   bytes preserve source identities. No host matrix limit narrows a program.
+
+**Process-image conformance (K85; suites C/D/F/G).**
+
+1. **Domain bytes and scope (producer/reader/checker).** Compare absent
+   process domain, explicit empty fixed_regions and one nonempty image.
+   The first two denote unrestricted D; the last fixes only the named in
+   mem slot, retaining full target/fault/borrowed/control/mut ranges. Exercise
+   multi-cell non-byte-aligned packing and padding, mem-slot order, wrong
+   role/shape/name, duplicate bindings, stale raw-byte hashes and a forbidden
+   bundle slice. Malformed records reject; legal huge images on an unable
+   host report unchecked, never evidence of a smaller D. For the existing
+   replay claim whose fixed_regions order is [aux,db], attach images in
+   canonical [db,aux] mem-slot order: the complete resolved bindings agree.
+   Exercise either replay list order with canonical attachment images;
+   comparison does not rewrite either claim's bytes. Missing, extra, duplicate,
+   wrong-slot or unequal shape/bytes/hash bindings reject.
+2. **Reduced input, complete output (checker).** Let a two-qubit interface
+   fix the second bit to zero, V=I4 and U=I2 tensor X. Then J_I has shape
+   4-by-2 and `(U−V)J_I` has Frobenius norm 2 (four entries of magnitude 1).
+   A numerical bound below 2 rejects under this procedure; 2 passes exact
+   interval arithmetic. The output fixed-bit leakage remains visible. The
+   channel witness is 8-by-8 and Tr_out is 2-by-2, tracing four output
+   states. Reject a 4-by-4 witness that silently reduced the output too.
+3. **Phase and interval procedures (checker).** With the same isometry and
+   U=-V, induced channels agree, but `(U−V)J_I` has Frobenius norm sqrt(8)
+   and the phase-sensitive numerical claim with bound 0 rejects. Exercise
+   all off-diagonal units with an external reference and strict positive
+   interval pivots. Missing or extra per-context duals reject, and an
+   inconclusive numerical/SDP check never becomes a successful image bound.
+4. **Logical preparation (checker).** Allocate zero cells, apply X on set
+   image bits and forward them to the subject; verify exact factorisation,
+   entry image and exit restoration. Include a checked nontrivial logical
+   preparation. Insert an unlisted intervening entangler, change the mapped
+   mem slot or replace allocation with unknown coherent data: the attachment
+   fails even with unchanged declared bytes/hash. Exercise both matrix_units
+   and an earlier exact restoration claim; sampled, approximate, circular
+   and reference-only substitutes for realised restoration do not suffice.
+   Round-trip two visits to the same preparation point in one qloop and two
+   fixed-binding instances of one lproc row in the same oracle step: complete
+   addresses differ. Include distinct oracle steps/phases and nested calls;
+   stale terminal coordinates or a mismatched symbol reject. At $construct,
+   address allocation and multiple image-preparation leaves for each of two
+   local qregions by generated ordinal and forward allocation address; all
+   resolve uniquely, including raw reversal with retained forward identities
+   and a reference-only construction. A source point without its complete
+   leaf address, duplicate complete address or mismatched allocation rejects.
+   For realised native X = [[3/5,4/5],[4/5,-3/5]], epsilon 1, source-only
+   zero-then-X preparation declares image 1 but the actual state has probability
+   9/25 outside it. Retain an independently proved conditional identity-callee
+   theorem and its exact image restoration, but grant no executable applicability
+   from that ideal preparation. Check the bound root prefix, including an
+   unlisted scheduled intervening gate. Also accept a positive-epsilon
+   realisation whose realised prefix provably preserves the exact entry image
+   and factorisation; unavailable realisation mechanics leave applicability
+   unestablished without changing source legality.
+5. **Launch-copy association (launch provider/checker).** Use the same bytes
+   from a native database and snapshot to prepare a fresh device factor.
+   Observe copied packing, actual root/context/mem-slot/handle association,
+   lifetime and mutation exclusion through completion. A stale manifest hash,
+   copy index, schedule, actual handle or changed image invalidates the use;
+   a producer boolean or hash of unknown coherent state cannot establish it.
+   A static template without checked runtime association remains conditional.
+6. **Contexts and reuse (checker/executor).** Two calls to one closure,
+   including default-covered, coherently disabled and source-adjoint calls,
+   need their own complete attachments; one copied key cannot cover both.
+   Change nested args, token_aliases, budget, variant, control count, root,
+   target or schedule independently and observe refusal to discharge that
+   invocation with the stale result. Unchanged conditional theorems may be
+   reused, but a new launch still establishes fresh preparation/association;
+   restoration of the original image is checked before any valid reuse.
+   A callee with a different mapped image leaves the parent's composed error
+   obligation unestablished even when the callee's isolated image bound passed.
+7. **Verdicts, identity and mixed scope (reader/checker/provider).** Without
+   preparation, retain the successful conditional theorem/bound and report
+   applicability unestablished; unavailable target/interval mechanics remain
+   Unverified. Malformed/refuted attachments reject; unsupported descriptor
+   versions never confer applicability. No image result proves full-D borrow
+   or inverse obligations. Changing domain, witness or manifest bytes changes
+   the certificate/cache identity (and manifest hash when applicable), with
+   unchanged source/header/target/schedule identities preserved. Two embedded
+   device roots carry separate bindings; native main/libc need no fabricated
+   device certificate and a missing mixed transport reports its actual gap.
+
 **Suite H / §11.1 K77 adapter vector.** Captured `oracle_invocation`
 follows the source call's arguments and body/template capture, irrespective
 of unrelated apply-site context; nested calls restore the enclosing context
```

## Author rationale (.tmp/isa-textdefects/RATIONALE.md)
# Contract draft rationale

This is an in-version ISA 0.9 text-defect draft at the orchestrator's explicit
request, restricted to §8.3 native models, §12.1 numerical/channel payload rows,
§12.3 binding text and new §15 groups. No header, K ledger, ABI header,
implementation, catalog or 0.8-to-0.9 diff was edited. The published-contract
review/council and full gate belong to the orchestrator; the contract is not
claimed council-accepted merely because publication checks pass. The legacy
spec/README version-bump prescription is superseded for this job by the explicit
in-version defect brief and its K91 precedent, not silently generalized to
other edits. Private files here are not to be committed or backed up publicly.

## Readings preserved from the reference interpreter

Read the required K86 progress in full, SPEC-QUESTIONS.md in full and the
K86 branch's native/expression reconstruction read-only. Preserve the existing
reduced rational leaves, finite AST operators and exact binary64 rational
binding; k/c/eps/theta meanings; base target permutations; own/effective to
allocation permutation; MSB-first individual-wire indices; controlled_U's
identity-disabled construction and phase; exact native accuracy vs separate
certificate Frobenius/SDP obligations; no positive-epsilon ideal fallback.

Unimplemented models/identities stay unchecked. Numerical/channel executable
checks remain Unverified when required machinery is unavailable; image-only
theorems alone do not establish invocation applicability. There was no current
oracle encoding for the missing representations or preparation attachment to
preserve. No implementation or conformance vectors for these new formats are
claimed: b-isa-spec-0ib and b-isa-spec-qrc remain required.

## Alternatives and decisions for review/council

- **Representation identity and phase.** A bare Kraus/instrument/environment
  representation could identify only a channel and lose global phase. Keep
  the existing phase-bearing data.matrix as U; add an optional discriminated
  representation beside it, not a replacement kind. Logical channel equality
  is checked on every matrix unit; native epsilon/control phase is separate.
  Instruments discard only their classical outcome, environment matrices only
  their explicitly named environment outputs. A mixed environment density
  matrix is allowed, rather than silently fixing a pure zero state.
- **Actual controls.** Arbitrary control of individual Kraus operators is
  unsound. Preserve controlled_U as the target author's actual-implementation
  binding; add explicit full-context Operation rows selected by disjoint c
  ranges. Expressions retain k/eps/theta dependence. Ranges plus symbolic
  Size/Basis/Map and matrix constructors cover unbounded admitted c without
  enumerating infinitely many matrices. Top-level full-context arity/basis
  agree with the pre-existing explicit-model prose. Unbounded means no new
  algorithm-domain limit, not that a host must materialise infinite data.
- **Matrix portability.** Dense-only matrices would contradict the existing
  symbolic-generation promise. The finite, closed constructor set has exact
  algebraic semantics; it does not introduce a general executable generator,
  arbitrary code, plugin URI, opaque blob or cross-repo code dependency.
  Different exact expressions/constructors may denote the same operation;
  canonical means unambiguous JCS bytes per supplied tree, not a canonical
  representative of mathematical equivalence classes.
- **Optional certificates.** Rather than an opaque proof string or a producer
  success flag, publish closed versions for an exact Gram witness and dense
  rational enclosure. The checker independently proves both Gram equalities
  or rigorous containment. These witnesses do not invent a symbolic theorem
  prover or permit interval overlap to prove equality. Unsupported exact
  identities stay unchecked as in the existing interpreter. Certifying U
  does not waive separate environment/state/representation obligations.
- **Process domain.** Reusing replay domains would import omission-at-zero
  slices accidentally. A new versioned process-domain embeds exactly the
  existing fixed_regions image format and keeps every other input unrestricted.
  Omission retains old unrestricted semantics and bytes. Explicitly fixing an
  in image reduces inputs only; complete output and arbitrary external
  references remain observable. A conditional numerical result is a process
  bound, not an exact permutation or restoration proof.
- **Preparation vs theorem.** A serializable producer boolean or image hash
  cannot establish factorisation of an unknown coherent input. Attach a
  versioned witness separately to each claim/context/invocation. Logical
  witnesses resolve actual allocation/preparation occurrences and the entire
  intervening program; launch-copy templates require a checked runtime
  association to a fresh clean factor and actual copied classical bytes.
  Neither route narrows source legality or inspects unknown coherent data.
- **Runtime boundary.** Defining a new C pointer/handle transport here would
  collide with the unresolved mixed-object ABI. A closed hash-bound logical
  by-value ImageLaunch manifest defines the input data; the existing mixed
  boundary still supplies transport/ownership. Static template validation is
  explicitly insufficient for actual future launch applicability. Missing
  mechanics are reported unestablished, not an executable success or illegal
  source program. Provider-private actual handle association is not serialized.
- **Restoration/reuse/composition.** Approximate closeness does not prove
  exact exit image restoration. Independently reconstruct it on matrix units
  or use an earlier applicable exact full-tuple/permutation theorem. No
  circular, sampled or approximate substitutes. Each launch re-establishes
  preparation; theorem caches match all immutable bindings, not just bytes.
  Conditional callee bounds enter error/multiplicity composition only after
  each actual mapped image/preparation/restoration obligation is established.

## Role/observable audit of new MUSTs

Numbers are the exact order checked by check_contract.py: native completion,
then the two payload rows, then the new binding block. Existing surrounding
K86 MUSTs are unchanged. N1..N7/P1..P7 name the new §15 conformance groups.
This audit now includes the two fix-round MUSTs for full occurrence resolution
and realised-prefix preparation; numbering below follows the final text.

| # | Role | Observable | §15 group |
|---|---|---|---|
| 1 | Model producer | Exact field set and canonical JCS bytes | N1 |
| 2 | Model reader | Reject malformed known-format fields/types | N1 |
| 3 | Model reader | Reject invalid rational/AST/binding/Size | N1 |
| 4 | Checker | Reject incompatible matrix shapes, no padding | N1 |
| 5 | Model reader | Reject bad arity/basis/map | N5 |
| 6 | Checker | Identity-derived row/column permutation | N5 |
| 7 | Model reader | Exactly one explicit context selected or reject | N4 |
| 8 | Checker | PSD trace-one state, unitary dilation, correct reduced map | N3 |
| 9 | Checker | TP Kraus sum and all-matrix-unit equality | N2 |
| 10 | Checker | Independent unitarity and phase-sensitive epsilon | N2/N4 |
| 11 | Checker | Independent outward enclosure contained in box | N6 |
| 12 | Checker | Exact gram=U†U=I; interval overlap never suffices | N6 |
| 13 | Checker | Unsupported representation/constructor/certificate is unchecked | N7 |
| 14 | Checker | Actual contextual U/V and proper full/reduced Frobenius comparison | P2/P3 |
| 15 | Checker | Bound only when all contexts pass, scope reported | P3/P6 |
| 16 | Checker | Exactly one dual per context with proper rectangular dimensions | P2/P3 |
| 17 | Checker | Rigorous strict pivots and finite nonnegative mu/bound | P3 |
| 18 | Certificate producer | Fixed image list in mem-slot order | P1 |
| 19 | Checker | Resolve/reject wrong role, shape, padding or hash | P1 |
| 20 | Checker | Report applicability separately from conditional theorem | P7 |
| 21 | Certificate reader | Unique concrete leaf/lifetime, no wildcard/stale terminal or allocation identity | P4 |
| 22 | Certificate reader | Reject stale/conflicting/malformed attachment | P1/P6 |
| 23 | Checker | Prove entry image/factorisation using actual logical operations | P4 |
| 24 | Checker | Actual scheduled root prefix proves exact entry image/factorisation; source-only preparation insufficient | P4 |
| 25 | Launch provider | Validate manifest and actually prepare fresh factor | P5 |
| 26 | Launch provider | Exclude mutation/rebinding through invocation | P5 |
| 27 | Checker | Independently establish exact exit image/factorisation | P4 |
| 28 | Reader/checker | Unsupported/unavailable attachment leaves applicability unestablished | P7 |
| 29 | Executor | Use theorem only for matching bindings with entry/exit checked | P6 |
| 30 | Composition checker | Require mapped preparation/restoration before using conditional bounds | P6/P7 |
| 31 | Producer/reader | Hash/cache new certificate bytes; preserve unchanged artifact identities | P7 |

## Evidence limits

check_contract.py verifies publication anchors, scope and the audit, including
deliberate broken-contract mutations; it is not a general schema parser or
proof of prose consistency. check_witnesses.py uses independent Fraction
arithmetic (no interpreter imports) for the Kraus/environment/phase and
reduced-input/full-output examples. The unchanged ref catalog check validates
the existing 219 recipes, not new-format decoder or executable applicability.
No new matrices/vectors or executable checks were added to implementation
paths. No full gate, review, council, merge or main push was performed here.

## Fix-round choices after integration with main

A single Occurrence names a public pre-target expansion leaf using the terminal
symbol/iteration/instance/step/phase/generated coordinates in addition to the
containing context. K83 leaves require a closed Allocation record naming the
forward acquisition leaf. This supplies interoperable lifetime bytes without
serialising a private scratch id or introducing a borrowed-frame (K89) schema.
Source-level points alone never select all expansions. The bound schedule's
library or the reference default determines public ordinals; target models
then reconstruct realised leaves. Raw trace inversion retains public forward
identities, whereas source-adjoint formation uses its own published coordinates.

K85 replay fixed_regions preserves producer order. Equality against an ordered
attachment compares all resolved binding data after mem-slot normalization,
matching 73a68c8 images09.rs's BTreeMap order; no interpreter change required.

Logical preparation remains expressible for loops, lproc instances and local
regions, and now explicitly proves the bound realised root prefix before
executable use. Ideal source proofs do not establish entry for approximate X
that leaks 9/25 out of image 1. Positive advertised epsilon does not prohibit
a proof when the actual prefix exactly prepares/factorises the image.

The reviews contain no P2/nit findings. Their follow-on decoding, numerical,
runtime/applicability and vector requests remain required implementation work
under 0ib/qrc, documented in the fix progress for the orchestrator.

## Fix-round record (.tmp/isa-textdefects-fix/PROGRESS.md)
# Resume

Updated: 2026-11-09T09:46:51Z

## Done

Final head b08940d2b6fa04e7322befe2e8f98b91a1055caf, branch job/isa-textdefects-u94-rqn. Merge 1f873602e5284c5a85f540def623d5ecf443a0d9 plus fix b08940d2b6fa04e7322befe2e8f98b91a1055caf. Both end Agent: gpt-6.1-sol; origin wip/isa-textdefects is the exact final head (ls-remote receipt). Tracked tree clean; only private .tmp untracked. No running command.

Ran exactly git -C /home/tobias/Projects/bennett-workspace/bennett-isa-spec-job-textdefects merge --no-ff main; main was 695cb4b7c330742820c6b315337a260e56de8bce. Preserved K85 73a68c8 and K91 1b46f93.
Combined hunks (complete inventory): ONE content conflict at the §15 insertion before Suite H / §11.1 K77. Kept all nine Loader-capability conformance (K91) groups first, then all seven Native representation (K86) and seven Process-image (K85) groups. No text discarded. K91 §10.1 and ledger auto-merged unchanged.
Fix edits ONLY spec/Bennett-ISA-Spec-0.9.md §12.3 and the owned §15 process groups. No interpreter/conformance/diff edits; merge inherited those from main. No private files committed.

Finding closure (final spec line numbers):
- SOL-TEXT-01 + astra F1: Occurrence 4878 and Allocation 4882 are closed complete terminal leaf / forward-acquisition records. §12.3 4899–4945 gives symbol/interface hash, qloop iteration, fixed instance, terminal step/phase presence, public bound-library generated ordinal, K83 required allocation identity, reference default, reversal and unique resolution. Complete-address duplicate checks follow. §15 P4 5756 includes repeated loop visits, lproc instances, steps/phases, nested calls, two local regions/multiple support leaves, stale coordinates, reference-only and raw inversion. Symbol follows existing §9.2/§11 interface-hash coordinates, confirmed by interpreter source-schedule test text; no new closure-hash selector invented.
- SOL-TEXT-02: §12.3 4956–4966 compares complete resolved (mem slot,A,W,raw bytes,hash) bindings after canonical ordering; producer replay order/bytes unchanged, attachment canonical order retained. §15 P1 5730 accepts [aux,db] replay with [db,aux] attachment and rejects missing/extra/duplicate/unequal bindings. Default reading matches 73a68c8 images09.rs BTreeMap resolution; no interpreter change required.
- astra F2: §12.3 4989 proves actual realised preparation and full intervening root prefix from bound schedule, resolved contexts and target models before executable applicability. Source-only proofs cannot establish a different prefix. Positive epsilon remains permitted when exact image/factorisation is proved. §15 P4 includes rational-X leakage 9/25, conditional identity-callee/restoration retention, unlisted actual gate, and positive-epsilon preservation.
- Both reviews contain NO P2/nit findings. All text-only minimal fixes applied; follow-on mechanics requested below. No scope narrowing, source legality change or ideal fallback.

## Verified

Receipts: .tmp/isa-textdefects-fix/verification.json (exact argv/cwd, head, UTC, wall/CPU, expected/actual exit, spec SHA-256) and check-*.txt. Run driver: python3 -I -B .tmp/isa-textdefects-fix/run_checks.py -> PASS all 13 checks on final committed head.
All commands headless, TMPDIR=<worktree>/.tmp/isa-textdefects-fix/tmp. No full gate/build and no sibling full gate.

Merge-head checks:
- Original check_contract.py --self-check passed 29 MUSTs but failed outside-scope because old 22dd3ab baseline lacks inherited K91. Private checker SCOPE_BASE updated to integrated main 695cb4b, leaving baseline-red source 22dd3ab and all scope exclusions unchanged. Re-run on merge head PASS: 29 MUSTs, 12 corruptions, 14 groups. check_witnesses.py PASS on merge head.
- Original reviewer scripts both re-run before fixing: both reproduced collisions; SOL reproduced array-order conflict; astra reproduced admissible epsilon-1 X leakage.
- check_revision.py first ran BEFORE spec edits and failed on missing terminal fields (revision-red.txt).

Final-head checks (all successful exits 0 except deliberately red cases):
- python3 -I -B .tmp/isa-textdefects/check_contract.py --baseline -> expected exit1 missing old encodings.
- python3 -I -B .tmp/isa-textdefects/check_contract.py --self-check -> PASS 31 MUST role/observable rows, 12 corruptions, 14 groups, exact outside-owned bytes against integrated main.
- python3 -I -B .tmp/isa-textdefects/check_witnesses.py -> PASS independent native/process Fraction arithmetic.
- python3 -I -B .tmp/isa-textdefects-fix/check_revision.py -> PASS closed fields, canonical equality, realised prefix and §15 regressions.
- python3 -I -B .tmp/isa-textdefects-fix/sol_probe.py -> "SOL terminal fixed-binding instances: 2 distinct addresses, no collision"; source symbols2 and oracle step/phase4 also no collision; [aux,db] replay equals [db,aux] attachment after full resolution; missing/unequal bindings differ.
- python3 -I -B .tmp/isa-textdefects-fix/astra_probe.py -> "astra qloop visits: 2 distinct addresses, no collision"; "astra K83 allocation/image leaves: 6 distinct addresses, no collision"; exact rational-X leakage9/25 and positive-epsilon -X image preservation PASS.
- Both revised probes with --baseline -> expected exit1 actual old-production collision. They project onto fields parsed from the published productions; same review input cases, now with required coordinates. Read-only original review sources untouched. These are encoding/arithmetic witnesses, not decoder tests or executable applicability proofs.
- python3 -I -B conformance/tools/ref_catalog.py --check -> PASS219; unchanged envelope 5de4e4995350313e50217880ba1b95de39cd043283b726337d4894efb005d197.
- git diff --exit-code 695cb4b HEAD -- reference-interpreter conformance spec/isa-0.8-to-0.9.diff -> PASS, all inherited unmodified.
- git diff --check 695cb4b..HEAD and git diff --exit-code HEAD -> PASS.
- git ls-remote --exit-code origin refs/heads/wip/isa-textdefects -> exact final head.

## Open / next

bennett-isa-spec-u94 and bennett-isa-spec-rqn remain in_progress pending round-2 review/council/publication; both now have determining comments with final commit/verification/acceptance boundary. Procedural deviation: the two comment writes were invoked from this worktree (shared database), contrary to T3CHILD's main-cwd rule; subsequent bd comments --json from MAIN confirmed both persisted correctly. No duplicate corrective comments or bead export committed. Merge pre-commit hook auto-exported the shared main database and warned no Dolt remote; no sync/remote repair attempted.

Bead requests for orchestrator / existing required mechanics (not new contract findings):
- b-isa-spec-0ib: implement all closed native-model representations, matrix constructors, context/operand binding and optional certificate decoding; exact unitarity, phase/accuracy, environment/CPTP matrix-unit equivalence, rigorous outward containment and unsupported-vs-malformed reporting. Publish actual seven native conformance groups' vectors; text checks do not establish a decoder.
- b-isa-spec-qrc: version-dispatched numerical/channel process-domain and bindings.preparation / image-launch readers, separate process vs replay domain validation (current metadata_schema lacks fields and certificate domain validator assumes replay regions). Preserve 0.8/unrestricted bytes and producer replay order.
- b-isa-spec-qrc: realised complete-context reconstruction, reduced-input/full-output numerical/Choi rigorous checks; unique concrete occurrence and K83 forward allocation/lifetime resolution; prove actual root preparation prefix, exact exit restoration, runtime copy/handle association and separate applicability reporting. Cache all bindings and validate every mapped callee before conditional error/multiplicity composition. Publish actual seven process-image groups' vectors. Missing mechanics remain Unverified/unestablished; no boolean/manifest hash alone grants success.
- Existing bennett-4ht mixed transport/ownership boundary remains required; this text defines no invented C ABI. No new cross-repo bead needed and no requested mechanics claimed complete.

Orchestrator next: fresh round-2 review/council disposition on b08940d, regenerate spec/isa-0.8-to-0.9.diff, full gate ONCE under receipt rules, export beads, merge/push/publication. No round 3. No PR, main push, subagents or external messages.
