The "environment_tools" library
===============================

Utilities for working with hierarchical environments, such as datacenters and
AWS regions grouped into logical environments, like prod, staging, dev.

This library primary reads two files: location_types.json and
location_mapping.json.

Examples
--------

An example environment might have a `location_types.json` that looks like this:

```json
["ecosystem", "superregion", "region", "habitat"]
```

These go from least specific (largest) to most specific (smallest).
The smaller location types (like habitat) are entirely enclosed within the larger types.

The `location_mapping.json` file should list every location in a tree structure, with the largest groupings (`ecosystem`, in the example above) as the root key, and the smaller structures nested as subkeys.
The smallest location types (`habitat` in the example) should have an empty dictionary as their value.

Example `location_mapping.json`:

```json
{
  "prod_ecosystem": {
    "pnw-prod_superregion": {
      "uswest2-prod_region": {
        "uswest2aprod_habitat": {},
        "uswest2bprod_habitat": {},
        "uswest2cprod_habitat": {}
      },
      "pdx-prod_region": {
        "pdx1_habitat": {},
      }
    },
    "nova-prod_superregion": {
      "useast1-prod_region": {
        "useast1aprod_habitat": {},
        "useast1bprod_habitat": {},
        "useast1cprod_habitat": {}
      },
      "iad-prod_region": {
        "iad1_habitat": {},
        "iad2_habitat": {}
      }
    }
  },
  "deva_ecosystem": {
    "norcal-deva_superregion": {
      "uswest1-deva_region": {
        "uswest1adeva_habitat": {},
        "uswest1bdeva_habitat": {}
      }
    }
  }
}
```

In this example, our production `ecosystem` has two `superregion`s, each containing an AWS region and one or more physical datacenters (pdx1, iad1, iad2).

Our `deva` ecosystem is much simpler, containing only one superregion with one AWS region.

Picking location types
----------------------

At Yelp, we defined the `ecosystem` as one distinct copy of our infrastructure.
All of production is one `ecosystem`, and then each staging environment or dev environment is its own `ecosystem`.
In general, an application running within one `ecosystem` should talk only to hosts and applications running within the same `ecosystem`.

To subdivide, we have `habitat`s for each AWS availability zone or physical datacenter cage within an ecosystem.
AWS regions become `region`s, and we define `region`s around physical datacenters.
Regions are then grouped together into `superregion`s, according to some latency bound.

Note that one physical datacenter or AZ can house multiple `habitat`s: there could be a `uswest1aprod` and a `uswest1adevb`, which are distinct from one another.

An application can then operate at the level of the hierarchy that makes the most sense for its latency and resource requirements.
A service with extremely tight latency requirements might choose to operate at the `habitat` level, speaking only with other instances within the same habitat.
A service with looser SLAs might operate at the `superregion` level, giving it more flexibility of where to run.
