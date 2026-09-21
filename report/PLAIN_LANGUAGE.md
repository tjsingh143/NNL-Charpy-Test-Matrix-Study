# The project in plain language

This is background for three readers: a professor who wants to know whether the reasoning holds, a
technical interviewer who wants to know whether the author understands what they did, and a
first-year engineering student who has not met any of this before. It explains the ideas. The
numbers, and the evidence behind them, are in `report/charpy_test_matrix_study.pdf`; every figure in
that report comes from `outputs/`, and every number in it is traceable through
`report/claim_source_map.csv` and `report/constant_source_map.csv`.

Nothing here was measured by this project. Every measurement came from published studies, and this
work analyses them.

---

## 1. Why steel can be tough one day and brittle the next

Most structural steels used in reactor pressure vessels are *ferritic*: their atoms sit in a
body-centred cubic arrangement. In that arrangement, the planes of atoms that slide past one another
to let the metal bend become much harder to move as the temperature falls. Below some temperature
the steel stops bending to absorb a blow and instead splits apart along crystal planes — cleavage.
Above it, the steel tears in a ductile way, soaking up far more energy.

The change is not gradual and it is not sharp either: it happens over a band of temperature called
the **ductile-to-brittle transition**. Austenitic stainless steels, whose atoms sit in a
face-centred cubic arrangement, have many more easy slip directions and keep deforming down to very
low temperatures, so they do not show this transition in the same way. That is why the austenitic
records in the dataset are excluded from this analysis: the model being fitted describes something
they do not do.

This matters for a reactor because a pressure vessel must never be in the brittle regime while it is
pressurised. Neutron irradiation pushes the transition to *higher* temperatures over the life of the
plant, so knowing where the transition sits, and how far it has moved, is a safety question.

## 2. What a Charpy test actually measures

A Charpy V-notch specimen is a small bar with a notch cut in one face. A pendulum swings down and
breaks it. The machine records how much energy the specimen absorbed, from how high the pendulum
swings afterwards.

Repeat this at many temperatures and the absorbed energies trace an S-shaped curve: low and flat at
cold temperatures (the **lower shelf**), rising through the transition, then high and flat again
(the **upper shelf**).

Two honest cautions come with that number:

- **Absorbed energy is an index, not a material property.** It depends on the specimen's size and
  shape, the notch, the striking speed and the machine. It is not a quantity you can feed into a
  stress calculation the way you would use yield strength or fracture toughness. It is a
  standardised, repeatable *indicator* that correlates with toughness.
- **Where you put the specimens matters as much as how many you have.** Specimens tested on the flat
  shelves tell you almost nothing about where the transition is. Only specimens in the sloping part
  pin it down.

## 3. Why 41 J, and what the transition temperature is for

The curve is summarised by a single **index temperature**: the temperature at which the fitted curve
crosses a chosen energy. For full-size reactor pressure vessel specimens the conventional choice is
**41 J**, because United States regulation defines the irradiation-induced shift in terms of the
41 J temperature measured before and after irradiation.

That shift feeds a reference temperature used to draw the pressure–temperature limits the plant is
operated within. So 41 J is not a physical threshold in the steel; it is a **regulatory convention**
chosen so that everybody computes the same number the same way. This report is careful never to
describe it as a material constant.

## 4. Why surveillance capsules exist, and why the material is precious

You cannot cut a test specimen out of an operating reactor vessel. So when the plant is built,
small capsules of the same steel are placed inside the vessel, closer to the core than the wall is,
so they receive neutron damage *faster* than the wall does. Every few years one capsule is removed
and its specimens are broken, giving a preview of where the vessel's transition temperature is
heading.

There is a fixed amount of that steel and no way to make more of it. Once a capsule is tested, it is
gone. **That scarcity is the whole reason this project exists.**

## 5. The actual question

A fixed volume of irradiated steel can be machined into a few full-size specimens, or into many
smaller ones. Which choice tells you more about the transition temperature?

It sounds obvious — more specimens must be better. It is not obvious, for one reason: a small
specimen does not behave like a scaled-down large one, so its answer has to be **corrected** back to
full-size behaviour, and that correction is imperfect.

## 6. Why a small specimen is not a small version of a big one

Two effects, both physical:

- **Constraint.** In a thick specimen, the material at the notch root is gripped by the material
  around it and cannot contract sideways. The stress state becomes strongly three-dimensional, which
  favours cleavage. A thin specimen can deform out of plane, behaves more ductilely at the same
  temperature, and so has a transition at a *lower* temperature. This is a temperature effect, and
  no energy scale factor can express it — which is exactly why a separate temperature correction is
  needed at all.
- **Weakest link.** Cleavage starts at the worst defect in the stressed volume. A bigger specimen
  samples more material, so it is more likely to contain a bad one, and fails brittly sooner.

There is also the plain fact that a smaller specimen breaks less steel, so it absorbs less energy.
*That* part a geometric factor can handle: the classical correction scales energy by a measure of
the ligament volume, and shifts temperature by a formula that depends on the same volume.

The correction helps a lot. It does not work perfectly, and the leftover disagreement is the number
this project has to measure.

## 7. What "the fit is ill-conditioned" means

Fitting the S-curve means choosing four numbers — two shelf levels, a mid-transition temperature and
a width — so the curve passes as near the measured points as possible.

If your specimens are all on the shelves, many different curves fit them about equally well. The
data cannot tell those curves apart, so the transition temperature is barely determined even though
the fit "worked". That is **ill-conditioning**: the answer is not pinned down by the data, and a
fitting program will still happily print one.

This project therefore reports, for every curve, whether the sampling actually identified the
parameters, and refuses to quote an index temperature that falls outside the temperatures actually
tested. A number the data cannot support is not reported as if it could.

## 8. What a bootstrap is

You have one set of specimens and one answer. How much would that answer have moved if the
experiment had come out slightly differently?

The **bootstrap** answers this by building many pretend experiments from the data you already have —
drawing specimens at random, with repeats allowed — refitting each one, and looking at how much the
answer moves. The spread of those answers estimates the uncertainty.

Its limit is the key to this whole project: a bootstrap can only capture variation it can *see* in
the data. It measures scatter and sampling luck. It cannot measure an error that affects every
specimen in the programme identically.

## 9. The error floor, and why it does not average away

The size correction is exactly such a shared error. It is one formula, applied to one material. It
either suits that material or it does not, and testing more specimens does not find out.

So the two kinds of error behave completely differently as specimens are added:

- **Curve-fitting error** shrinks roughly as one over the square root of the number of specimens.
  Four times as many specimens, half the error.
- **Size-correction error** does not shrink at all.

A miniature programme's total error therefore falls with specimen count only until it meets the
correction error, and then it stops. That is the **error floor** — about 12 °C under this project's
central assumptions (report §6.4; key `floor.central` in `report/claim_source_map.csv`). A full-size
programme has no such floor, because it needs no correction.

The answer to the research question follows directly. When the material budget is very small, the
full-size programme has so few specimens that its fitting error is worse than the miniature floor,
and the small specimens win. As the budget grows, the full-size error keeps falling, crosses the
floor, and keeps going. So miniature specimens help at small budgets and full-size dominates as the
budget rises.

## 10. Why the answer is stated with conditions

Three honest limits sit on that conclusion, and the report states all three wherever the result
appears:

1. **The correction distribution rests on very few independent materials.** Matching a miniature
   curve to a full-size curve of the *same* heat, condition and study is rare in this compilation.
   Only a handful of genuinely matched families exist, and **no individual miniature geometry has
   enough evidence to support its own correction** — so one pooled correction is used for all of
   them, which the data can neither confirm nor refute.
2. **The specimens are miniaturized, not conventional sub-size.** The relevant standard treats those
   as different things. The dataset's only two conventional reduced-thickness sub-size curves are
   too sparse to use, so this work says nothing about them rather than guessing.
3. **The volume accounting is idealised.** It counts how many finished specimens fit in a block of
   steel. It does not model capsule layout, machining losses or holder geometry.

There is also a physical limit that no assumption can argue away: a miniature specimen's correction
shifts its effective temperature upward, so for a material whose transition is very cold, the
smaller specimen **cannot be tested cold enough to see its own transition at all**, even in liquid
nitrogen. For those materials the question is not which size is more precise; it is whether the
small one can be used.

## 11. The one-sentence version

Spending scarce irradiated steel on many small Charpy specimens buys a better-sampled curve but
imports a size-correction error that more specimens cannot reduce, so small specimens help only
while the material budget is very small, and the most valuable thing that could improve the
trade-off is not more small specimens but better matched full-size-to-miniature correction data.
