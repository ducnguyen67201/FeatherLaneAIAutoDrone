# Turning a request into flight actions

[Core architecture](../architecture/README.md) · [Master learning plan](../MASTER-LEARNING-PLAN.md)


Recorded 2026-10-31 in response to the user's clarification example: select a location, fly slowly, find an ice cream truck and land beside it. This page explains a proposed simulation workflow. It does not approve new implementation, deploy a system or establish that natural-language interpretation, autonomous search or landing-site selection already works. Native mission ownership and optional perception retain their previously confirmed scope. Use the maintained core architecture for module placement; this page explains task behavior and is not flight evidence or design approval.

## From wording to an executable contract

A form, mission template or optional language interpreter translates the request into a typed mission. A model may propose the interpretation outside time-critical flight callbacks. Native admission validates the resulting contract against supported capabilities and limits; raw language cannot directly actuate the vehicle.

| Request meaning | Required explicit interpretation |
| --- | --- |
| Fly here | GPS/local destination, coordinate frame, altitude reference and allowed operating region. A point alone does not define a search area. |
| Go slowly | A named, qualified motion profile with actual speed, acceleration, jerk and stopping limits. |
| Find the truck | Target definition, intended-instance rule, bounded search region or corridor, viewing coverage, termination conditions and required perception/localization. |
| Do not explore, if requested | Restrict movement and observations to the specified route/region; do not expand the search silently. Report not found if those limits prevent acquisition. |
| Land beside it | A separate reachable landing region outside the object, adequate surface/clearance evidence and a valid descent corridor. |
| When completion is impossible | Explicit, feasible fallback for a blocked route, absent target, insufficient remaining energy, invalid inputs or unavailable landing site. |

Missing information can come from explicit operator input or an already approved mission template. Unresolved ambiguity stays visible. For example, without a destination/search region or an accepted prior about the truck's location, the system has no justified direction to fly. Arbitrary geographic search must not be invented from the word “find.” Exact schema, model choice and interpretation interface remain discovery decisions.

## Choosing where to go before the target is visible

The next destination is an observation location, not the unknown truck position. Within the permitted region, a search policy chooses candidate viewpoints that are reachable and likely to reveal unobserved space. It uses the map, camera field of view, visibility/occlusion, previous observations and mission limits. An initial implementation can use predefined observation points or a coverage route; it does not require a learned search policy.

At each observation location, the system evaluates the scene, records what was actually observable, and selects another permitted viewpoint if the target has not been confirmed. Looking at a building wall does not establish that the area behind it was searched. Remaining time/energy, return reserve, required input validity and geographic limits bound this loop. If exploration is prohibited, the search is restricted to the allowed route/viewpoints. A target-not-found outcome is a valid result.

The task-level search policy decides the next objective; a route planner decides how to reach it. Heavy mapping/planning/perception can supply bounded candidates from external compute. The native C++ coordinator owns progression, acceptance and fallback; existing ArduPilot estimation/navigation/controllers retain their qualified responsibilities.

## Handling trees and buildings

Known map obstacles can influence the route before movement. Live depth/proximity observations update a local occupied/free/unknown-space representation as the vehicle moves. That representation is distinct from semantic truck detection. An ordinary RGB image box does not establish metric clearance.

The route planner considers vehicle extent, uncertainty, limits and stopping space. It proposes a route around observed/known obstacles while remaining inside the permitted region and altitude limits. Navigation/reference generation turns that route into feasible timed motion. State-feedback control continually corrects execution. Newly observed obstacles may cause slowing, replanning or the configured feasible fallback. The system cannot assume it can always go over a building, squeeze through a gap or reach an occluded region.

ArduPilot offers [BendyRuler](https://ardupilot.org/copter/docs/common-oa-bendyruler.html) for local path planning with documented inputs and AUTO/GUIDED/RTL mode constraints. Its [Dijkstra avoidance](https://ardupilot.org/copter/docs/common-oa-dijkstras.html) handles configured fences/stay-out zones, rather than live lidar/proximity obstacles. These are conditional reuse candidates, not a ready-made general urban planner. Our proposed custom mode must explicitly integrate and qualify any reused avoidance path.

## Finding the truck changes the active step

A candidate detection is checked against the target definition and intended instance. A generic vehicle detector alone does not establish “ice cream truck.” Depending on the scenario, appearance recognition, markings or an operator-provided reference could support identification; those capabilities need separate evaluation.

A confirmed object still needs qualified spatial localization. The mission selects an approach/staging region outside its occupied volume and follows it using the same route/reference/control machinery. Required observations and identity checks remain active under the mission's explicit loss policy. This example assumes a stationary truck in simulation; moving-target pursuit is not silently added.

## Landing is a separate capability

Landing beside a recognized truck requires evidence about the ground, not merely the truck. Candidate sites must provide suitable surface/footprint, clearance from the truck and other obstacles, and a usable approach/descent corridor. A road, occupied patch, roof or unobserved surface is not automatically acceptable because it is close to the target.

The mission can evaluate another site within its permitted search/landing limits. Without a qualified site, it reports that landing cannot be completed and applies the configured feasible fallback; holding/returning depends on current navigation and vehicle capability. If a site is admitted, the selected ArduPilot landing path executes descent and the mission checks actual touchdown/terminal state. A command acknowledgment is not touchdown.

ArduPilot [precision landing](https://ardupilot.org/copter/docs/precision-landing-and-loiter.html) can use external landing-target measurements with valid navigation and appropriate configuration. It does not by itself discover or certify an arbitrary clear patch beside an object. Landing-target guidance and landing-site selection are separate responsibilities.

## What this adds to discovery

The existing P03 known-goal motion, P04 optional object perception and P05 route/arrival work remain useful foundations. A full “find and land” demonstration additionally needs explicit request interpretation, bounded search/viewpoint selection and landing-site assessment/descent qualification. These are discovery requirements exposed by the example, not completed capabilities or new approved phase gates. The current approach-and-hold criteria do not prove them. No Word export or approved design is replaced by this explanatory child page.
