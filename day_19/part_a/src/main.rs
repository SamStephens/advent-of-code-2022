use std::{io, cmp};
use regex::{Regex, Captures};

const LAST_MINUTE: u16 = 24;

#[derive(Debug, Clone)]
struct ResourceSet {
    ore: u16,
    clay: u16,
    obsidian: u16,
    geode: u16,
}

#[derive(Debug, Clone)]
struct Blueprint {
    identifier: u16,
    robots: Vec<Robot>
}

#[derive(Debug, Clone)]
struct Robot {
    cost: ResourceSet,
    production: ResourceSet,
}

impl ResourceSet {
    fn can_produce_eventually(&self, cost: &ResourceSet) -> bool {
        if cost.ore > 0 && self.ore == 0 {
            return false;
        }
        if cost.clay > 0 && self.clay == 0 {
            return false;
        }
        if cost.obsidian > 0 && self.obsidian == 0 {
            return false;
        }
        if cost.geode > 0 && self.geode == 0 {
            return false;
        }
        return true;
    }

    fn add_production(&mut self, production: &ResourceSet) {
        self.ore += production.ore;
        self.clay += production.clay;
        self.obsidian += production.obsidian;
        self.geode += production.geode;
    }

    fn can_afford(&self, cost: &ResourceSet) -> bool {
        if cost.ore > self.ore {
            return false;
        }
        if cost.clay > self.clay {
            return false;
        }
        if cost.obsidian > self.obsidian {
            return false;
        }
        if cost.geode > self.geode {
            return false;
        }
        return true;
    }

    fn spend_cost(&mut self, cost: &ResourceSet) {
        self.ore -= cost.ore;
        self.clay -= cost.clay;
        self.obsidian -= cost.obsidian;
        self.geode -= cost.geode;
    }
}

fn parse_capture(captures: &Captures, index: usize) -> u16 {
    let value = captures.get(index).expect("Missing group in capture").as_str();
    let value: u16 = value.parse().expect("Expected capture group to be a number");
    return value;
}

fn read_blueprints() -> Vec<Blueprint> {
    let lines = io::stdin().lines();
    let re = Regex::new(r"^Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.$").unwrap();
    let mut blueprints: Vec<Blueprint> = Vec::new();
    for line in lines {
        let line = line.unwrap();
        let captures = re.captures(&line).expect("Capture failed");
        let identifier = parse_capture(&captures, 1);
        let ore_robot_ore = parse_capture(&captures, 2);
        let clay_robot_ore = parse_capture(&captures, 3);
        let obsidian_robot_ore = parse_capture(&captures, 4);
        let obsidian_robot_clay = parse_capture(&captures, 5);
        let geode_robot_ore = parse_capture(&captures, 6);
        let geode_robot_obsidian = parse_capture(&captures, 7);
        blueprints.push(Blueprint {
            identifier: identifier,
            robots: vec![
                Robot {
                    cost: ResourceSet { ore: ore_robot_ore, clay: 0, obsidian: 0, geode: 0 },
                    production: ResourceSet { ore: 1, clay: 0, obsidian: 0, geode: 0 },
                },
                Robot {
                    cost: ResourceSet { ore: clay_robot_ore, clay: 0, obsidian: 0, geode: 0 },
                    production: ResourceSet { ore: 0, clay: 1, obsidian: 0, geode: 0 },
                },
                Robot {
                    cost: ResourceSet { ore: obsidian_robot_ore, clay: obsidian_robot_clay, obsidian: 0, geode: 0 },
                    production: ResourceSet { ore: 0, clay: 0, obsidian: 1, geode: 0 },
                },
                Robot {
                    cost: ResourceSet { ore: geode_robot_ore, clay: 0, obsidian: geode_robot_obsidian, geode: 0 },
                    production: ResourceSet { ore: 0, clay: 0, obsidian: 0, geode: 1 },
                },
            ],
        });
    }
    return blueprints;
}

fn robot_does_not_help_production(robots: &Vec<Robot>, robot: &Robot, production: &ResourceSet) -> bool {
    if robot.production.geode > 0 {
        return false;
    }

    if robot.production.ore > 0 {
        if robots.iter().any(|r| r.cost.ore > production.ore) {
            return false;
        }
    }

    if robot.production.clay > 0 {
        if robots.iter().any(|r| r.cost.clay > production.clay) {
            return false;
        }
    }

    if robot.production.obsidian > 0 {
        if robots.iter().any(|r| r.cost.obsidian > production.obsidian) {
            return false;
        }
    }

    return true;
}

fn max_geodes_for_robots(
    robots: &Vec<Robot>,
    production: ResourceSet,
    stocks: ResourceSet,
    minute: u16,
) -> u16 {
    let mut max_geodes = (LAST_MINUTE - minute) * production.geode;
    for robot in robots {
        if !production.can_produce_eventually(&robot.cost) {
            continue;
        }

        if robot_does_not_help_production(&robots, &robot, &production) {
            continue;
        }

        let mut next_minute = minute;
        let mut next_stocks = stocks.clone();

        while !next_stocks.can_afford(&robot.cost) {
            next_minute += 1;
            next_stocks.add_production(&production);
        }

        next_minute += 1;

        if next_minute >= LAST_MINUTE {
            continue;
        }

        next_stocks.add_production(&production);
        next_stocks.spend_cost(&robot.cost);
        let mut next_production = production.clone();
        next_production.add_production(&robot.production);

        let max_geodes_after_minute = max_geodes_for_robots(
            &robots,
            next_production,
            next_stocks,
            next_minute,
        );

        max_geodes = cmp::max(
            production.geode * (next_minute - minute) + max_geodes_after_minute,
            max_geodes,
        );
    }
    return max_geodes;
}

fn main() {
    let blueprints = read_blueprints();
    let mut quality_level_sum: u32 = 0;
    for blueprint in blueprints {
        let max_geodes = max_geodes_for_robots(
            &blueprint.robots,
            ResourceSet { ore: 1, clay: 0, obsidian: 0, geode: 0 },
            ResourceSet { ore: 0, clay: 0, obsidian: 0, geode: 0 },
            0,
        );
        quality_level_sum += (blueprint.identifier as u32) * (max_geodes as u32);
    }
    println!("{:?}", quality_level_sum);
}
