<template>
  <v-row justify="center">
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="primary" dark v-bind="attrs" v-on="on"> Open Dialog </v-btn>
    </template>
    <v-card>
      <v-card-text>
        <div class="col-md-12">
          <h1>G-code Index</h1>
          <br>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.0.0-beta</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <h2>
              <a href="/docs/gcode/G000-G001.html">G0-G1 - Linear Move</a>
            </h2>
            <p>Add a straight line movement to the planner</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.0.0-beta</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <h2>
              <a href="/docs/gcode/G002-G003.html"
                >G2-G3 - Arc or Circle Move</a
              >
            </h2>
            <p>Add an arc or circle movement to the planner</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.0.0-beta</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <h2><a href="/docs/gcode/G004.html">G4 - Dwell</a></h2>
            <p>Pause the planner</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-warning"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Experimental feature"
                ><i class="fa fa-flask" aria-hidden="true"></i></span
            ></span>
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <h2>
              <a href="/docs/gcode/G005.html">G5 - Bézier cubic spline</a>
            </h2>
            <p>Cubic B-spline with XYZE destination and IJPQ offsets</p>
          </div>
          <div class="gcode item">
            <span class="label label-warning"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Experimental feature"
                ><i class="fa fa-flask" aria-hidden="true"></i></span
            ></span>
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <span class="label label-requires"
              ><code>DIRECT_STEPPING</code></span
            >
            <h2>
              <a href="/docs/gcode/G006.html">G6 - Direct Stepper Move</a>
            </h2>
            <p>
              Perform a direct, uninterpolated, and non-kinematic synchronized
              move
            </p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.0.0-beta</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <span class="label label-requires"><code>FWRETRACT</code></span>
            <h2><a href="/docs/gcode/G010.html">G10 - Retract</a></h2>
            <p>Retract the filament</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.0.0-beta</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <span class="label label-requires"><code>FWRETRACT</code></span>
            <h2><a href="/docs/gcode/G011.html">G11 - Recover</a></h2>
            <p>Recover the filament with firmware-based retract.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-warning"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Experimental feature"
                ><i class="fa fa-flask" aria-hidden="true"></i></span
            ></span>
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> nozzle</span
            >
            <span class="label label-requires"
              ><code>NOZZLE_CLEAN_FEATURE</code></span
            >
            <h2><a href="/docs/gcode/G012.html">G12 - Clean the Nozzle</a></h2>
            <p>Perform the nozzle cleaning procedure.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> geometry</span
            >
            <span class="label label-requires"
              ><code>CNC_WORKSPACE_PLANES</code></span
            >
            <h2>
              <a href="/docs/gcode/G017-G019.html"
                >G17-G19 - CNC Workspace Planes</a
              >
            </h2>
            <p>Select CNC workspace plane</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> units</span
            >
            <span class="label label-requires"
              ><code>INCH_MODE_SUPPORT</code></span
            >
            <h2><a href="/docs/gcode/G020.html">G20 - Inch Units</a></h2>
            <p>Set Units to Inches.</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> units</span
            >
            <span class="label label-requires"
              ><code>INCH_MODE_SUPPORT</code></span
            >
            <h2><a href="/docs/gcode/G021.html">G21 - Millimeter Units</a></h2>
            <p>Set Units to Millimeters.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-warning"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Experimental feature"
                ><i class="fa fa-flask" aria-hidden="true"></i></span
            ></span>
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"><code>HAS_MESH</code></span>
            <span class="label label-requires"
              ><code>G26_MESH_VALIDATION</code></span
            >
            <h2>
              <a href="/docs/gcode/G026.html">G26 - Mesh Validation Pattern</a>
            </h2>
            <p>Test the mesh and adjust.</p>
          </div>
          <div class="gcode item">
            <span class="label label-warning"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Experimental feature"
                ><i class="fa fa-flask" aria-hidden="true"></i></span
            ></span>
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> nozzle</span
            >
            <span class="label label-requires"
              ><code>NOZZLE_PARK_FEATURE</code></span
            >
            <h2><a href="/docs/gcode/G027.html">G27 - Park toolhead</a></h2>
            <p>Park the current toolhead</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <h2><a href="/docs/gcode/G028.html">G28 - Auto Home</a></h2>
            <p>Auto home one or more axes.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>AUTO_BED_LEVELING_3POINT</code></span
            >
            <h2>
              <a href="/docs/gcode/G029-abl-3point.html"
                >G29 - Bed Leveling (3-Point)</a
              >
            </h2>
            <p>Probe the bed and enable leveling compensation.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>AUTO_BED_LEVELING_BILINEAR</code></span
            >
            <h2>
              <a href="/docs/gcode/G029-abl-bilinear.html"
                >G29 - Bed Leveling (Bilinear)</a
              >
            </h2>
            <p>Probe the bed and enable leveling compensation.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>AUTO_BED_LEVELING_LINEAR</code></span
            >
            <h2>
              <a href="/docs/gcode/G029-abl-linear.html"
                >G29 - Bed Leveling (Linear)</a
              >
            </h2>
            <p>Probe the bed and enable leveling compensation.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>MESH_BED_LEVELING</code></span
            >
            <h2>
              <a href="/docs/gcode/G029-mbl.html"
                >G29 - Bed Leveling (Manual)</a
              >
            </h2>
            <p>Measure Z heights in a grid, enable leveling compensation</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>AUTO_BED_LEVELING_UBL</code></span
            >
            <h2>
              <a href="/docs/gcode/G029-ubl.html"
                >G29 - Bed Leveling (Unified)</a
              >
            </h2>
            <p>Probe the bed and enable leveling compensation.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code
                >AUTO_BED_LEVELING_(3POINT|LINEAR|BILINEAR|UBL)|MESH_BED_LEVELING</code
              ></span
            >
            <h2><a href="/docs/gcode/G029.html">G29 - Bed Leveling</a></h2>
            <p>Probe the bed and enable leveling compensation</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.0.0-beta</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"><code>HAS_BED_PROBE</code></span>
            <h2><a href="/docs/gcode/G030.html">G30 - Single Z-Probe</a></h2>
            <p>Probe bed at current XY location</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.0.0-beta</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"><code>Z_PROBE_SLED</code></span>
            <h2><a href="/docs/gcode/G031.html">G31 - Dock Sled</a></h2>
            <p>Dock the Z probe sled.</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.0.0-beta</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"><code>Z_PROBE_SLED</code></span>
            <h2><a href="/docs/gcode/G032.html">G32 - Undock Sled</a></h2>
            <p>Undock the Z probe sled.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i>
              calibrationdelta</span
            >
            <span class="label label-requires"
              ><code>DELTA_AUTO_CALIBRATION</code></span
            >
            <h2>
              <a href="/docs/gcode/G033.html">G33 - Delta Auto Calibration</a>
            </h2>
            <p>Calibrate various Delta parameters</p>
          </div>
          <div class="gcode item">
            <span class="label label-warning"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Experimental feature"
                ><i class="fa fa-flask" aria-hidden="true"></i></span
            ></span>
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>Z_STEPPER_AUTO_ALIGN</code></span
            >
            <h2>
              <a href="/docs/gcode/G034.html"
                >G34 - Z Steppers Auto-Alignment</a
              >
            </h2>
            <p>Align multiple Z steppers using a bed probe</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>ASSISTED_TRAMMING</code></span
            >
            <h2>
              <a href="/docs/gcode/G035.html">G35 - Tramming Assistant</a>
            </h2>
            <p>Run a procedure to tram the bed</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>G38_PROBE_TARGET</code></span
            >
            <h2>
              <a href="/docs/gcode/G038.html">G38.2-G38.5 - Probe target</a>
            </h2>
            <p>Probe towards (or away from) a workpiece</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.2</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"><code>HAS_MESH</code></span>
            <h2>
              <a href="/docs/gcode/G042.html">G42 - Move to mesh coordinate</a>
            </h2>
            <p>Move to a specific point in the leveling mesh</p>
          </div>
          <div class="gcode item">
            <span class="label label-warning"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Experimental feature"
                ><i class="fa fa-flask" aria-hidden="true"></i></span
            ></span>
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> geometry</span
            >
            <span class="label label-requires"
              ><code>CNC_COORDINATE_SYSTEMS</code></span
            >
            <h2>
              <a href="/docs/gcode/G053.html"
                >G53 - Move in Machine Coordinates</a
              >
            </h2>
            <p>Apply native workspace to the current move.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-warning"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Experimental feature"
                ><i class="fa fa-flask" aria-hidden="true"></i></span
            ></span>
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> geometry</span
            >
            <span class="label label-requires"
              ><code>CNC_COORDINATE_SYSTEMS</code></span
            >
            <h2>
              <a href="/docs/gcode/G054-G059.html"
                >G54-G59.3 - Workspace Coordinate System</a
              >
            </h2>
            <p>Select a workspace coordinate system</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> coordinates</span
            >
            <h2>
              <a href="/docs/gcode/G060.html">G60 - Save Current Position</a>
            </h2>
            <p>Save current position to specified slot</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> coordinates</span
            >
            <h2>
              <a href="/docs/gcode/G061.html">G61 - Return to Saved Position</a>
            </h2>
            <p>Return to saved position of specified slot</p>
          </div>
          <div class="gcode item">
            <span class="label label-warning"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Experimental feature"
                ><i class="fa fa-flask" aria-hidden="true"></i></span
            ></span>
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>PROBE_TEMP_COMPENSATION</code></span
            >
            <h2>
              <a href="/docs/gcode/G076.html"
                >G76 - Probe temperature calibration</a
              >
            </h2>
            <p>Calibrate probe temperature compensation</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <span class="label label-requires"
              ><code>GCODE_MOTION_MODES</code></span
            >
            <h2>
              <a href="/docs/gcode/G080.html"
                >G80 - Cancel Current Motion Mode</a
              >
            </h2>
            <p>Cancel the current motion mode</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.0.0-beta</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> units</span
            >
            <h2>
              <a href="/docs/gcode/G090.html">G90 - Absolute Positioning</a>
            </h2>
            <p>Set the interpreter to absolute positions</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.0.0-beta</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> units</span
            >
            <h2>
              <a href="/docs/gcode/G091.html">G91 - Relative Positioning</a>
            </h2>
            <p>Set the interpreter to relative positions</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.0.0-beta</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <h2><a href="/docs/gcode/G092.html">G92 - Set Position</a></h2>
            <p>Set the current position of one or more axes.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-warning"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Experimental feature"
                ><i class="fa fa-flask" aria-hidden="true"></i></span
            ></span>
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>CALIBRATION_GCODE</code></span
            >
            <h2>
              <a href="/docs/gcode/G425.html">G425 - Backlash Calibration</a>
            </h2>
            <p>Use a conductive object to calibrate XYZ backlash</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> debug</span
            >
            <span class="label label-requires"
              ><code>DEBUG_GCODE_PARSER</code></span
            >
            <h2>
              <a href="/docs/gcode/G800.html">G800-M800 - Debug Gcode Parser</a>
            </h2>
            <p>Returns Gcode data</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.0.0-beta</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <h2>
              <a href="/docs/gcode/M000-M001.html"
                >M0-M1 - Unconditional stop</a
              >
            </h2>
            <p>Stop and wait for user</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.2</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>SPINDLE_LASER_ENABLE</code></span
            >
            <h2>
              <a href="/docs/gcode/M003.html">M3 - Spindle CW / Laser On</a>
            </h2>
            <p>Set the spindle CW speed or laser power</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.2</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>SPINDLE_LASER_ENABLE</code></span
            >
            <h2>
              <a href="/docs/gcode/M004.html">M4 - Spindle CCW / Laser On</a>
            </h2>
            <p>Set the spindle CCW speed or laser power</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.2</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>SPINDLE_LASER_ENABLE</code></span
            >
            <h2>
              <a href="/docs/gcode/M005.html">M5 - Spindle / Laser Off</a>
            </h2>
            <p>Turn off spindle or laser</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> Coolant
              Controls</span
            >
            <h2>
              <a href="/docs/gcode/M007-M009.html">M7-M9 - Coolant Controls</a>
            </h2>
            <p>Turn mist or flood coolant on / off</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 2.0.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> safety</span
            >
            <span class="label label-requires"
              ><code>EXPECTED_PRINTER_CHECK</code></span
            >
            <h2>
              <a href="/docs/gcode/M016.html">M16 - Expected Printer Check</a>
            </h2>
            <p>Prevent G-code usage on the wrong machine</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <h2><a href="/docs/gcode/M017.html">M17 - Enable Steppers</a></h2>
            <p>Enable steppers</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <h2>
              <a href="/docs/gcode/M018.html">M18, M84 - Disable steppers</a>
            </h2>
            <p>Disable steppers (same as M84).</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <span class="label label-requires"><code>SDSUPPORT</code></span>
            <h2><a href="/docs/gcode/M020.html">M20 - List SD Card</a></h2>
            <p>List the contents of the SD Card.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <span class="label label-requires"><code>SDSUPPORT</code></span>
            <h2><a href="/docs/gcode/M021.html">M21 - Init SD card</a></h2>
            <p>Attempt to detect an SD card in the slot.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <span class="label label-requires"><code>SDSUPPORT</code></span>
            <h2><a href="/docs/gcode/M022.html">M22 - Release SD card</a></h2>
            <p>Simulate ejection of the SD card</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <span class="label label-requires"><code>SDSUPPORT</code></span>
            <h2><a href="/docs/gcode/M023.html">M23 - Select SD file</a></h2>
            <p>Select an SD file to be executed</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <span class="label label-requires"><code>SDSUPPORT</code></span>
            <h2>
              <a href="/docs/gcode/M024.html">M24 - Start or Resume SD print</a>
            </h2>
            <p>
              Start or resume a file selected with
              [`M23`](/docs/gcode/M023.html)
            </p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <span class="label label-requires"><code>SDSUPPORT</code></span>
            <h2><a href="/docs/gcode/M025.html">M25 - Pause SD print</a></h2>
            <p>Pause printing from the SD card</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <span class="label label-requires"><code>SDSUPPORT</code></span>
            <h2><a href="/docs/gcode/M026.html">M26 - Set SD position</a></h2>
            <p>Set the SD read position</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <span class="label label-requires"><code>SDSUPPORT</code></span>
            <h2>
              <a href="/docs/gcode/M027.html">M27 - Report SD print status</a>
            </h2>
            <p>Print SD progress to serial</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <span class="label label-requires"><code>SDSUPPORT</code></span>
            <h2><a href="/docs/gcode/M028.html">M28 - Start SD write</a></h2>
            <p>Start writing to a file on the SD card</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <span class="label label-requires"><code>SDSUPPORT</code></span>
            <h2><a href="/docs/gcode/M029.html">M29 - Stop SD write</a></h2>
            <p>Stop writing the file, end logging.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <h2><a href="/docs/gcode/M030.html">M30 - Delete SD file</a></h2>
            <p>Delete a specified file from SD.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> printjob</span
            >
            <h2><a href="/docs/gcode/M031.html">M31 - Print time</a></h2>
            <p>Report the current print time.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-warning"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Experimental feature"
                ><i class="fa fa-flask" aria-hidden="true"></i></span
            ></span>
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <span class="label label-requires"><code>SDSUPPORT</code></span>
            <h2><a href="/docs/gcode/M032.html">M32 - Select and Start</a></h2>
            <p>Begin an SD print from a file.</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.0.2</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <span class="label label-requires"><code>SDSUPPORT</code></span>
            <span class="label label-requires"
              ><code> LONG_FILENAME_HOST_SUPPORT</code></span
            >
            <h2><a href="/docs/gcode/M033.html">M33 - Get Long Path</a></h2>
            <p>Convert a short pathname to a long pathname.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <span class="label label-requires"><code>SDSUPPORT</code></span>
            <span class="label label-requires"
              ><code>SDCARD_SORT_ALPHA</code></span
            >
            <h2><a href="/docs/gcode/M034.html">M34 - SDCard Sorting</a></h2>
            <p>Set SDCard file sorting options.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <h2><a href="/docs/gcode/M042.html">M42 - Set Pin State</a></h2>
            <p>Set an analog or digital pin to a specified state.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-warning"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Experimental feature"
                ><i class="fa fa-flask" aria-hidden="true"></i></span
            ></span>
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> debug</span
            >
            <span class="label label-requires"
              ><code>PINS_DEBUGGING</code></span
            >
            <h2><a href="/docs/gcode/M043-T.html">M43 T - Toggle Pins</a></h2>
            <p>Get information about pins.</p>
          </div>
          <div class="gcode item">
            <span class="label label-warning"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Experimental feature"
                ><i class="fa fa-flask" aria-hidden="true"></i></span
            ></span>
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> debug</span
            >
            <span class="label label-requires"
              ><code>PINS_DEBUGGING</code></span
            >
            <h2><a href="/docs/gcode/M043.html">M43 - Debug Pins</a></h2>
            <p>Get information about pins.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>Z_MIN_PROBE_REPEATABILITY_TEST</code></span
            >
            <h2>
              <a href="/docs/gcode/M048.html">M48 - Probe Accuracy Test</a>
            </h2>
            <p>Measure Z Probe repeatability.</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.7</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> lcd</span
            >
            <span class="label label-requires"
              ><code>LCD_SET_PROGRESS_MANUALLY</code></span
            >
            <h2>
              <a href="/docs/gcode/M073.html">M73 - Set Print Progress</a>
            </h2>
            <p>Set current print progress percentage for LCD.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> printjob</span
            >
            <h2>
              <a href="/docs/gcode/M075.html">M75 - Start Print Job Timer</a>
            </h2>
            <p>Start the print job timer.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> printjob</span
            >
            <h2><a href="/docs/gcode/M076.html">M76 - Pause Print Job</a></h2>
            <p>Pause the print job timer.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> printjob</span
            >
            <h2>
              <a href="/docs/gcode/M077.html">M77 - Stop Print Job Timer</a>
            </h2>
            <p>Stop the print job timer.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> printjob</span
            >
            <span class="label label-requires"><code>PRINTCOUNTER</code></span>
            <h2><a href="/docs/gcode/M078.html">M78 - Print Job Stats</a></h2>
            <p>Print statistics about print jobs.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"><code>PSU_CONTROL</code></span>
            <h2><a href="/docs/gcode/M080.html">M80 - Power On</a></h2>
            <p>Turn on the power supply</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"><code>PSU_CONTROL</code></span>
            <h2><a href="/docs/gcode/M081.html">M81 - Power Off</a></h2>
            <p>Turn off the power supply.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> units</span
            >
            <h2><a href="/docs/gcode/M082.html">M82 - E Absolute</a></h2>
            <p>Set E to absolute positioning.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> units</span
            >
            <h2><a href="/docs/gcode/M083.html">M83 - E Relative</a></h2>
            <p>Set E to relative positioning.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <h2>
              <a href="/docs/gcode/M085.html">M85 - Inactivity Shutdown</a>
            </h2>
            <p>Set the inactivity timeout.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <h2>
              <a href="/docs/gcode/M092.html">M92 - Set Axis Steps-per-unit</a>
            </h2>
            <p>Set the number of steps-per-mm or steps-per-inch.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> debug</span
            >
            <span class="label label-requires"
              ><code>M100_FREE_MEMORY_WATCHER</code></span
            >
            <h2><a href="/docs/gcode/M100.html">M100 - Free Memory</a></h2>
            <p>Observe memory used by code</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> internal</span
            >
            <span class="label label-requires"
              ><code>POWER_LOSS_RECOVERY</code></span
            >
            <h2>
              <a href="/docs/gcode/M1000.html">M1000 - Internal Use Only</a>
            </h2>
            <p>Resume from Power Loss</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> internal</span
            >
            <span class="label label-requires"><code>SDSUPPORT</code></span>
            <h2>
              <a href="/docs/gcode/M1001.html">M1001 - Internal Use Only</a>
            </h2>
            <p>Run SD Print Finishing Actions</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> thermal</span
            >
            <h2>
              <a href="/docs/gcode/M104.html">M104 - Set Hotend Temperature</a>
            </h2>
            <p>Set a new target hot end temperature.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> thermal</span
            >
            <h2>
              <a href="/docs/gcode/M105.html">M105 - Report Temperatures</a>
            </h2>
            <p>Send a temperature report to the host.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> thermal</span
            >
            <span class="label label-requires"
              ><code>EXTRA_FAN_SPEED</code></span
            >
            <h2><a href="/docs/gcode/M106.html">M106 - Set Fan Speed</a></h2>
            <p>Turn on the fan and set its speed</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> thermal</span
            >
            <h2><a href="/docs/gcode/M107.html">M107 - Fan Off</a></h2>
            <p>Turn off a fan</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <h2>
              <a href="/docs/gcode/M108.html">M108 - Break and Continue</a>
            </h2>
            <p>Break out of the current waiting loop</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> thermal</span
            >
            <h2>
              <a href="/docs/gcode/M109.html"
                >M109 - Wait for Hotend Temperature</a
              >
            </h2>
            <p>Wait for the hot end to reach its target.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> hosts</span
            >
            <h2><a href="/docs/gcode/M110.html">M110 - Set Line Number</a></h2>
            <p>Set the current line number.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> hosts</span
            >
            <h2><a href="/docs/gcode/M111.html">M111 - Debug Level</a></h2>
            <p>Report and optionally set the debug flags.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> safety</span
            >
            <h2><a href="/docs/gcode/M112.html">M112 - Emergency Stop</a></h2>
            <p>Shut everything down and halt the machine.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> hosts</span
            >
            <span class="label label-requires"
              ><code>HOST_KEEPALIVE_FEATURE</code></span
            >
            <h2><a href="/docs/gcode/M113.html">M113 - Host Keepalive</a></h2>
            <p>Get or set the host keepalive interval.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> hosts</span
            >
            <h2>
              <a href="/docs/gcode/M114.html">M114 - Get Current Position</a>
            </h2>
            <p>Report the current tool position to the host.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> hosts</span
            >
            <h2><a href="/docs/gcode/M115.html">M115 - Firmware Info</a></h2>
            <p>Print the firmware info and capabilities.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> lcd</span
            >
            <span class="label label-requires"><code>ULTRA_LCD</code></span>
            <h2><a href="/docs/gcode/M117.html">M117 - Set LCD Message</a></h2>
            <p>Set the message line on the LCD.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> hosts</span
            >
            <h2><a href="/docs/gcode/M118.html">M118 - Serial print</a></h2>
            <p>Send text to serial</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> debug</span
            >
            <h2><a href="/docs/gcode/M119.html">M119 - Endstop States</a></h2>
            <p>Report endstop and probe states to the host.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <h2><a href="/docs/gcode/M120.html">M120 - Enable Endstops</a></h2>
            <p>Enable endstops and keep them enabled when not homing.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <h2><a href="/docs/gcode/M121.html">M121 - Disable Endstops</a></h2>
            <p>Disable endstops and keep them enabled when not homing.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.7</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> debug</span
            >
            <span class="label label-requires"
              ><code>HAS_TRINAMIC_CONFIG</code></span
            >
            <h2><a href="/docs/gcode/M122.html">M122 - TMC Debugging</a></h2>
            <p>Get TMC Debug Info</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> nozzle</span
            >
            <span class="label label-requires"
              ><code>PARK_HEAD_ON_PAUSE</code></span
            >
            <h2><a href="/docs/gcode/M125.html">M125 - Park Head</a></h2>
            <p>Save current position and move to filament change position.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> baricuda</span
            >
            <span class="label label-requires"><code>BARICUDA</code></span>
            <h2><a href="/docs/gcode/M126.html">M126 - Baricuda 1 Open</a></h2>
            <p>Open the valve for Baricuda 1.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> baricuda</span
            >
            <span class="label label-requires"><code>BARICUDA</code></span>
            <h2><a href="/docs/gcode/M127.html">M127 - Baricuda 1 Close</a></h2>
            <p>Close the valve for Baricuda 1.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> baricuda</span
            >
            <span class="label label-requires"><code>BARICUDA</code></span>
            <h2><a href="/docs/gcode/M128.html">M128 - Baricuda 2 Open</a></h2>
            <p>Open the valve for Baricuda 2.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> baricuda</span
            >
            <span class="label label-requires"><code>BARICUDA</code></span>
            <h2><a href="/docs/gcode/M129.html">M129 - Baricuda 2 Close</a></h2>
            <p>Close the valve for Baricuda 2.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> thermal</span
            >
            <h2>
              <a href="/docs/gcode/M140.html">M140 - Set Bed Temperature</a>
            </h2>
            <p>Set a new target bed temperature.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> thermal</span
            >
            <h2>
              <a href="/docs/gcode/M141.html">M141 - Set Chamber Temperature</a>
            </h2>
            <p>Set a new target chamber temperature.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> lcd</span
            >
            <span class="label label-requires"><code>NEWPANEL</code></span>
            <h2>
              <a href="/docs/gcode/M145.html">M145 - Set Material Preset</a>
            </h2>
            <p>Set material presets in the LCD menu.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> units</span
            >
            <h2>
              <a href="/docs/gcode/M149.html">M149 - Set Temperature Units</a>
            </h2>
            <p>Set temperature units to Celsius, Fahrenheit, or Kelvin.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> lcd</span
            >
            <span class="label label-requires"
              ><code>BLINKM|RGB_LED|RGBW_LED|NEOPIXEL_LED|PCA9632</code></span
            >
            <h2><a href="/docs/gcode/M150.html">M150 - Set RGB(W) Color</a></h2>
            <p>Set the color of the RGB(W) LED, backlight, or LED strip.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> hosts</span
            >
            <span class="label label-requires"
              ><code>AUTO_REPORT_TEMPERATURES</code></span
            >
            <span class="label label-requires"
              ><code>EXTENDED_CAPABILITIES_REPORT</code></span
            >
            <h2>
              <a href="/docs/gcode/M155.html">M155 - Temperature Auto-Report</a>
            </h2>
            <p>Auto-report temperatures to host periodically.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> mixing</span
            >
            <span class="label label-requires"
              ><code>MIXING_EXTRUDER</code></span
            >
            <h2><a href="/docs/gcode/M163.html">M163 - Set Mix Factor</a></h2>
            <p>Set a single mix factor for a mixing extruder.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> mixing</span
            >
            <span class="label label-requires"
              ><code>MIXING_EXTRUDER</code></span
            >
            <span class="label label-requires"
              ><code>MIXING_VIRTUAL_TOOLS</code></span
            >
            <h2><a href="/docs/gcode/M164.html">M164 - Save Mix</a></h2>
            <p>Save the current mix as a virtual tool.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> mixing</span
            >
            <span class="label label-requires"
              ><code>MIXING_EXTRUDER</code></span
            >
            <span class="label label-requires"
              ><code>DIRECT_MIXING_IN_G1</code></span
            >
            <h2><a href="/docs/gcode/M165.html">M165 - Set Mix</a></h2>
            <p>Set all mix factors for the mixing extruder.</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 2.0.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> mixing</span
            >
            <span class="label label-requires"
              ><code>MIXING_EXTRUDER</code></span
            >
            <span class="label label-requires"><code>GRADIENT_MIX</code></span>
            <h2><a href="/docs/gcode/M166.html">M166 - Gradient Mix</a></h2>
            <p>Set a Gradient Mix</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> thermal</span
            >
            <h2>
              <a href="/docs/gcode/M190.html"
                >M190 - Wait for Bed Temperature</a
              >
            </h2>
            <p>Wait for the bed to reach target temperature.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> thermal</span
            >
            <h2>
              <a href="/docs/gcode/M191.html"
                >M191 - Wait for Chamber Temperature</a
              >
            </h2>
            <p>Wait for the chamber to reach target temperature.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 2.0.6.2</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>PROBE_TEMP_COMPENSATION</code></span
            >
            <h2>
              <a href="/docs/gcode/M192.html"
                >M192 - Wait for Probe temperature</a
              >
            </h2>
            <p>Wait for the probe temperature sensor to reach a target</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <h2>
              <a href="/docs/gcode/M200.html">M200 - Set Filament Diameter</a>
            </h2>
            <p>Set the diameter for volumetric extrusion.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <h2>
              <a href="/docs/gcode/M201.html"
                >M201 - Set Print Max Acceleration</a
              >
            </h2>
            <p>Set maximum acceleration for print moves one or more axes.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <h2><a href="/docs/gcode/M203.html">M203 - Set Max Feedrate</a></h2>
            <p>Set maximum feedrate for one or more axes.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <h2>
              <a href="/docs/gcode/M204.html"
                >M204 - Set Starting Acceleration</a
              >
            </h2>
            <p>Set the starting acceleration for moves by type.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <h2>
              <a href="/docs/gcode/M205.html">M205 - Set Advanced Settings</a>
            </h2>
            <p>Set some advanced settings related to movement.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <span class="label label-requires"
              ><code>HAS_HOME_OFFSET</code></span
            >
            <h2><a href="/docs/gcode/M206.html">M206 - Set Home Offsets</a></h2>
            <p>Apply a persistent offset</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <span class="label label-requires"><code>FWRETRACT</code></span>
            <h2>
              <a href="/docs/gcode/M207.html">M207 - Set Firmware Retraction</a>
            </h2>
            <p>Set options for firmware-based retraction.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <span class="label label-requires"><code>FWRETRACT</code></span>
            <h2><a href="/docs/gcode/M208.html">M208 - Firmware Recover</a></h2>
            <p>Firmware-retraction recover settings.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <span class="label label-requires"><code>FWRETRACT</code></span>
            <h2><a href="/docs/gcode/M209.html">M209 - Set Auto Retract</a></h2>
            <p>Enable / disable auto-retraction.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <span class="label label-requires"
              ><code>(MIN|MAX)_SOFTWARE_ENDSTOPS</code></span
            >
            <h2>
              <a href="/docs/gcode/M211.html">M211 - Software Endstops</a>
            </h2>
            <p>Set and/or get the software endstops state</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 2.0.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>EXTRUDERS &gt; 1</code></span
            >
            <h2>
              <a href="/docs/gcode/M217.html"
                >M217 - Filament swap parameters</a
              >
            </h2>
            <p>Set length and speed for filament swapping</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>EXTRUDERS&gt;1</code></span
            >
            <h2>
              <a href="/docs/gcode/M218.html">M218 - Set Hotend Offset</a>
            </h2>
            <p>Set the offset of a hotend (from hotend 0).</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <h2>
              <a href="/docs/gcode/M220.html">M220 - Set Feedrate Percentage</a>
            </h2>
            <p>Set the global feedrate percentage.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <h2>
              <a href="/docs/gcode/M221.html">M221 - Set Flow Percentage</a>
            </h2>
            <p>Set the flow percentage, which applies to all E moves.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <h2>
              <a href="/docs/gcode/M226.html">M226 - Wait for Pin State</a>
            </h2>
            <p>Wait for a pin to have a given state.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> extras</span
            >
            <span class="label label-requires"><code>PHOTO_GCODE</code></span>
            <h2><a href="/docs/gcode/M240.html">M240 - Trigger Camera</a></h2>
            <p>Trigger a camera shutter</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> lcd</span
            >
            <span class="label label-requires"
              ><code>HAS_LCD_CONTRAST</code></span
            >
            <h2><a href="/docs/gcode/M250.html">M250 - LCD Contrast</a></h2>
            <p>Set and/or get the LCD contrast.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> i2c</span
            >
            <span class="label label-requires"
              ><code>EXPERIMENTAL_I2CBUS</code></span
            >
            <h2><a href="/docs/gcode/M260.html">M260 - I2C Send</a></h2>
            <p>Send data to the I2C bus.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> i2c</span
            >
            <span class="label label-requires"
              ><code>EXPERIMENTAL_I2CBUS</code></span
            >
            <h2><a href="/docs/gcode/M261.html">M261 - I2C Request</a></h2>
            <p>Request and echo bytes from the I2C bus.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> servos</span
            >
            <span class="label label-requires"
              ><code>NUM_SERVOS&gt;0</code></span
            >
            <h2><a href="/docs/gcode/M280.html">M280 - Servo Position</a></h2>
            <p>Set or get a servo position.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> servos</span
            >
            <span class="label label-requires"
              ><code>EDITABLE_SERVO_ANGLES</code></span
            >
            <h2>
              <a href="/docs/gcode/M281.html">M281 - Edit Servo Angles</a>
            </h2>
            <p>Set servo deploy and/or stow angles</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.7</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"><code>BABYSTEPPING</code></span>
            <h2><a href="/docs/gcode/M290.html">M290 - Babystep</a></h2>
            <p>Babystep one or more axes</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> lcd</span
            >
            <span class="label label-requires"><code>SPEAKER</code></span>
            <h2><a href="/docs/gcode/M300.html">M300 - Play Tone</a></h2>
            <p>Play a single tone, buzz, or beep.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> thermal</span
            >
            <span class="label label-requires"><code>PIDTEMP</code></span>
            <h2><a href="/docs/gcode/M301.html">M301 - Set Hotend PID</a></h2>
            <p>Set PID values for a hotend.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> thermal</span
            >
            <span class="label label-requires"
              ><code>PREVENT_COLD_EXTRUSION</code></span
            >
            <h2><a href="/docs/gcode/M302.html">M302 - Cold Extrude</a></h2>
            <p>Set minimum extrusion temperature, allow cold extrusion.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> thermal</span
            >
            <span class="label label-requires"
              ><code>PIDTEMP|PIDTEMPBED</code></span
            >
            <h2><a href="/docs/gcode/M303.html">M303 - PID autotune</a></h2>
            <p>Auto-tune the PID system to find stable values.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> thermal</span
            >
            <span class="label label-requires"><code>PIDTEMPBED</code></span>
            <h2><a href="/docs/gcode/M304.html">M304 - Set Bed PID</a></h2>
            <p>Set PID values for the heated bed.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> thermal</span
            >
            <span class="label label-requires"
              ><code>temperature sensor `1000`</code></span
            >
            <h2>
              <a href="/docs/gcode/M305.html"
                >M305 - User Thermistor Parameters</a
              >
            </h2>
            <p>Set (or report) custom thermistor parameters</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>HAS_MICROSTEPS</code></span
            >
            <h2>
              <a href="/docs/gcode/M350.html">M350 - Set micro-stepping</a>
            </h2>
            <p>Set micro-stepping for drivers that support it</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>HAS_MICROSTEPS</code></span
            >
            <h2>
              <a href="/docs/gcode/M351.html">M351 - Set Microstep Pins</a>
            </h2>
            <p>Directly set the micro-stepping pins</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>CASE_LIGHT_PIN</code></span
            >
            <h2>
              <a href="/docs/gcode/M355.html">M355 - Case Light Control</a>
            </h2>
            <p>Turn the case light on or off, set brightness</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"><code>MORGAN_SCARA</code></span>
            <h2><a href="/docs/gcode/M360.html">M360 - SCARA Theta A</a></h2>
            <p>Move to Theta A</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"><code>MORGAN_SCARA</code></span>
            <h2><a href="/docs/gcode/M361.html">M361 - SCARA Theta-B</a></h2>
            <p>Move to Theta-B</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"><code>MORGAN_SCARA</code></span>
            <h2><a href="/docs/gcode/M362.html">M362 - SCARA Psi-A</a></h2>
            <p>Move to Psi-A</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"><code>MORGAN_SCARA</code></span>
            <h2><a href="/docs/gcode/M363.html">M363 - SCARA Psi-B</a></h2>
            <p>Move to Psi-B</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"><code>MORGAN_SCARA</code></span>
            <h2><a href="/docs/gcode/M364.html">M364 - SCARA Psi-C</a></h2>
            <p>Move to Psi-C</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> none</span
            >
            <span class="label label-requires"><code>EXT_SOLENOID</code></span>
            <h2>
              <a href="/docs/gcode/M380.html">M380 - Activate Solenoid</a>
            </h2>
            <p>Activate</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> none</span
            >
            <span class="label label-requires"><code>EXT_SOLENOID</code></span>
            <h2>
              <a href="/docs/gcode/M381.html">M381 - Deactivate Solenoids</a>
            </h2>
            <p>Deactivate all extruder solenoids</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <h2><a href="/docs/gcode/M400.html">M400 - Finish Moves</a></h2>
            <p>Wait for all moves to finish</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"><code>HAS_BED_PROBE</code></span>
            <h2><a href="/docs/gcode/M401.html">M401 - Deploy Probe</a></h2>
            <p>Deploy the bed probe</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"><code>HAS_BED_PROBE</code></span>
            <h2><a href="/docs/gcode/M402.html">M402 - Stow Probe</a></h2>
            <p>Stow the bed probe</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"><code>PRUSA_MMU2</code></span>
            <h2>
              <a href="/docs/gcode/M403.html">M403 - MMU2 Filament Type</a>
            </h2>
            <p>Set filament type for Multi-Material Unit 2.0</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>FILAMENT_WIDTH_SENSOR</code></span
            >
            <h2>
              <a href="/docs/gcode/M404.html">M404 - Set Filament Diameter</a>
            </h2>
            <p>Set the nominal diameter for filament width sensor auto-flow</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>FILAMENT_WIDTH_SENSOR</code></span
            >
            <h2>
              <a href="/docs/gcode/M405.html"
                >M405 - Filament Width Sensor On</a
              >
            </h2>
            <p>Enable filament width sensor flow control</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>FILAMENT_WIDTH_SENSOR</code></span
            >
            <h2>
              <a href="/docs/gcode/M406.html"
                >M406 - Filament Width Sensor Off</a
              >
            </h2>
            <p>Disable filament width sensor flow control</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>FILAMENT_WIDTH_SENSOR</code></span
            >
            <h2><a href="/docs/gcode/M407.html">M407 - Filament Width</a></h2>
            <p>Report the measured filament width</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <h2><a href="/docs/gcode/M410.html">M410 - Quickstop</a></h2>
            <p>Stop all steppers instantly</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 2.0.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>FILAMENT_RUNOUT_SENSOR</code></span
            >
            <h2><a href="/docs/gcode/M412.html">M412 - Filament Runout</a></h2>
            <p>Enable / disable filament runout detection</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 2.0.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>POWER_LOSS_RECOVERY</code></span
            >
            <h2>
              <a href="/docs/gcode/M413.html">M413 - Power-loss Recovery</a>
            </h2>
            <p>Enable / disable power-loss recovery</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <span class="label label-requires"
              ><code
                >AUTO_BED_LEVELING_(3POINT|LINEAR|BILINEAR|UBL)|MESH_BED_LEVELING</code
              ></span
            >
            <h2>
              <a href="/docs/gcode/M420.html">M420 - Bed Leveling State</a>
            </h2>
            <p>Get and/or set bed leveling state and parameters</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <span class="label label-requires"
              ><code
                >AUTO_BED_LEVELING_(BILINEAR|UBL)|MESH_BED_LEVELING</code
              ></span
            >
            <h2><a href="/docs/gcode/M421.html">M421 - Set Mesh Value</a></h2>
            <p>Set a single mesh Z height</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-warning"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Experimental feature"
                ><i class="fa fa-flask" aria-hidden="true"></i></span
            ></span>
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>Z_STEPPER_AUTO_ALIGN</code></span
            >
            <h2><a href="/docs/gcode/M422.html">M422 - Set Z Motor XY</a></h2>
            <p>Set a Z motor position for G34 Auto-Alignment</p>
          </div>
          <div class="gcode item">
            <span class="label label-warning"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Experimental feature"
                ><i class="fa fa-flask" aria-hidden="true"></i></span
            ></span>
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>BACKLASH_COMPENSATION</code></span
            >
            <span class="label label-requires"
              ><code>BACKLASH_GCODE</code></span
            >
            <h2>
              <a href="/docs/gcode/M425.html">M425 - Backlash compensation</a>
            </h2>
            <p>Enable and tune backlash compensation</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> motion</span
            >
            <span class="label label-requires"
              ><code>HAS_HOME_OFFSET</code></span
            >
            <h2>
              <a href="/docs/gcode/M428.html">M428 - Home Offsets Here</a>
            </h2>
            <p>Set home offsets based on current position</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> thermal</span
            >
            <span class="label label-requires"
              ><code
                >either POWER_MONITOR_CURRENT or POWER_MONITOR_VOLTAGE</code
              ></span
            >
            <h2><a href="/docs/gcode/M430.html">M430 - Power Monitor</a></h2>
            <p>Read and display current (A), voltage (V), and power (W)</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <span class="label label-requires"
              ><code>CANCEL_OBJECTS</code></span
            >
            <h2><a href="/docs/gcode/M486.html">M486 - Cancel Objects</a></h2>
            <p>Identify and cancel objects</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> eeprom</span
            >
            <span class="label label-requires"
              ><code>EEPROM_SETTINGS</code></span
            >
            <h2><a href="/docs/gcode/M500.html">M500 - Save Settings</a></h2>
            <p>Save settings to EEPROM.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> eeprom</span
            >
            <span class="label label-requires"
              ><code>EEPROM_SETTINGS</code></span
            >
            <h2><a href="/docs/gcode/M501.html">M501 - Restore Settings</a></h2>
            <p>Restore settings from EEPROM.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> eeprom</span
            >
            <h2><a href="/docs/gcode/M502.html">M502 - Factory Reset</a></h2>
            <p>Restore all settings to factory defaults.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> eeprom</span
            >
            <h2><a href="/docs/gcode/M503.html">M503 - Report Settings</a></h2>
            <p>Report all settings that may be saved to EEPROM.</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> eeprom</span
            >
            <span class="label label-requires"
              ><code>EEPROM_SETTINGS</code></span
            >
            <h2>
              <a href="/docs/gcode/M504.html"
                >M504 - Validate EEPROM contents</a
              >
            </h2>
            <p>Validate the contents of the EEPROM.</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 2.0.6.1</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> security</span
            >
            <span class="label label-requires"
              ><code>PASSWORD_FEATURE</code></span
            >
            <h2><a href="/docs/gcode/M510.html">M510 - Lock Machine</a></h2>
            <p>Lock the machine if it has a passcode</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 2.0.6.1</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> security</span
            >
            <span class="label label-requires"
              ><code>PASSWORD_FEATURE</code></span
            >
            <h2><a href="/docs/gcode/M511.html">M511 - Unlock Machine</a></h2>
            <p>Unlock the machine if it has a passcode</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 2.0.6.1</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> security</span
            >
            <span class="label label-requires"
              ><code>PASSWORD_FEATURE</code></span
            >
            <h2><a href="/docs/gcode/M512.html">M512 - Set Passcode</a></h2>
            <p>Set a numeric passcode for locking the machine</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 2.0.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <span class="label label-requires"><code>SDSUPPORT</code></span>
            <h2><a href="/docs/gcode/M524.html">M524 - Abort SD print</a></h2>
            <p>Abort an SD print started with [`M24`](/docs/gcode/M024.html)</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <span class="label label-requires"><code>SDSUPPORT</code></span>
            <span class="label label-requires"
              ><code>SD_ABORT_ON_ENDSTOP_HIT</code></span
            >
            <h2>
              <a href="/docs/gcode/M540.html">M540 - Endstops Abort SD</a>
            </h2>
            <p>Abort SD printing when an endstop is triggered.</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 2.0.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> none</span
            >
            <span class="label label-requires"
              ><code>TMC2130|TMC2208|TMC2209</code></span
            >
            <h2>
              <a href="/docs/gcode/M569.html">M569 - Set TMC stepping mode</a>
            </h2>
            <p>Toggle stealthChop</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 2.0.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> hosts</span
            >
            <span class="label label-requires"
              ><code>BAUD_RATE_GCODE</code></span
            >
            <h2><a href="/docs/gcode/M575.html">M575 - Serial baud rate</a></h2>
            <p>Change the serial baud rate</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> filament</span
            >
            <span class="label label-requires"
              ><code>ADVANCED_PAUSE_FEATURE</code></span
            >
            <h2><a href="/docs/gcode/M600.html">M600 - Filament Change</a></h2>
            <p>Automatically change filament</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.1.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> filament</span
            >
            <span class="label label-requires"
              ><code>ADVANCED_PAUSE_FEATURE</code></span
            >
            <h2>
              <a href="/docs/gcode/M603.html"
                >M603 - Configure Filament Change</a
              >
            </h2>
            <p>Configure automatic filament change parameters</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>DUAL_NOZZLE_DUPLICATION_MODE|DUAL_X_CARRIAGE</code></span
            >
            <h2><a href="/docs/gcode/M605.html">M605 - Dual Nozzle Mode</a></h2>
            <p>Set the behavior mode for dual nozzles</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> none</span
            >
            <span class="label label-requires"
              ><code>MORGAN_SCARA|MAKERARM_SCARA</code></span
            >
            <h2>
              <a href="/docs/gcode/M665-scara.html"
                >M665 - SCARA Configuration</a
              >
            </h2>
            <p>Set SCARA geometry values</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> none</span
            >
            <span class="label label-requires"><code>DELTA</code></span>
            <h2>
              <a href="/docs/gcode/M665.html">M665 - Delta Configuration</a>
            </h2>
            <p>Set delta geometry values</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>(X|Y|Z)_DUAL_ENDSTOPS</code></span
            >
            <h2>
              <a href="/docs/gcode/M666-dual.html"
                >M666 - Set dual endstop offsets</a
              >
            </h2>
            <p>Set dual endstop offsets</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"><code>DELTA</code></span>
            <h2>
              <a href="/docs/gcode/M666.html"
                >M666 - Set Delta endstop adjustments</a
              >
            </h2>
            <p>Set Delta endstop adjustments</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>DUET_SMART_EFFECTOR</code></span
            >
            <span class="label label-requires"
              ><code> SMART_EFFECTOR_MOD</code></span
            >
            <h2>
              <a href="/docs/gcode/M672.html">M672 - Test Speed Warning</a>
            </h2>
            <p>Set/clear Duet Smart Effector sensitivity</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>NOZZLE_PARK_FEATURE</code></span
            >
            <span class="label label-requires"
              ><code>ADVANCED_PAUSE_FEATURE</code></span
            >
            <span class="label label-requires"
              ><code>FILAMENT_LOAD_UNLOAD_GCODES</code></span
            >
            <h2><a href="/docs/gcode/M701.html">M701 - Load filament</a></h2>
            <p>Load filament</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>NOZZLE_PARK_FEATURE</code></span
            >
            <span class="label label-requires"
              ><code>ADVANCED_PAUSE_FEATURE</code></span
            >
            <span class="label label-requires"
              ><code>FILAMENT_LOAD_UNLOAD_GCODES</code></span
            >
            <h2><a href="/docs/gcode/M702.html">M702 - Unload filament</a></h2>
            <p>Unload filament</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 2.0.5.2</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> thermal</span
            >
            <span class="label label-requires"
              ><code>CONTROLLER_FAN_EDITABLE</code></span
            >
            <h2>
              <a href="/docs/gcode/M710.html">M710 - Controller Fan settings</a>
            </h2>
            <p>Set or report controller fan settings</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> debug</span
            >
            <span class="label label-requires"><code>MAX7219_DEBUG</code></span>
            <h2>
              <a href="/docs/gcode/M7219.html">M7219 - MAX7219 Control</a>
            </h2>
            <p>Control Max7219 Segmented LEDs</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 2.0.8</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> none</span
            >
            <span class="label label-requires"
              ><code>GCODE_REPEAT_MARKERS</code></span
            >
            <h2><a href="/docs/gcode/M808.html">M808 - Repeat Marker</a></h2>
            <p>Set or go to a marker for looping G-code</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-requires"><code>GCODE_MACROS</code></span>
            <h2>
              <a href="/docs/gcode/M810-M819.html">M810-M819 - G-code macros</a>
            </h2>
            <p>Set/execute one of ten G-code macros</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> none</span
            >
            <span class="label label-requires"><code>HAS_BED_PROBE</code></span>
            <h2><a href="/docs/gcode/M851.html">M851 - XYZ Probe Offset</a></h2>
            <p>Set the Z probe XYZ offset from nozzle</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-warning"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Experimental feature"
                ><i class="fa fa-flask" aria-hidden="true"></i></span
            ></span>
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <h2>
              <a href="/docs/gcode/M852.html">M852 - Bed Skew Compensation</a>
            </h2>
            <p>Misalignment in the XYZ axes.</p>
          </div>
          <div class="gcode item">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 1.0.0-beta</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> encoder</span
            >
            <span class="label label-requires"
              ><code>I2C_POSITION_ENCODERS</code></span
            >
            <h2>
              <a href="/docs/gcode/M860-M869.html"
                >M860-M869 - I2C Position Encoders</a
              >
            </h2>
            <p>I2C position encoders for closed loop control</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-warning"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Experimental feature"
                ><i class="fa fa-flask" aria-hidden="true"></i></span
            ></span>
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>PROBE_TEMP_COMPENSATION</code></span
            >
            <h2>
              <a href="/docs/gcode/M871.html"
                >M871 - Probe temperature config</a
              >
            </h2>
            <p>Configure probe temperature compensation</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> hosts</span
            >
            <span class="label label-requires"
              ><code>HOST_PROMPT_SUPPORT</code></span
            >
            <h2>
              <a href="/docs/gcode/M876.html">M876 - Handle Prompt Response</a>
            </h2>
            <p>Handle Host prompt responses</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"><code>LIN_ADVANCE</code></span>
            <h2>
              <a href="/docs/gcode/M900.html">M900 - Linear Advance Factor</a>
            </h2>
            <p>Get and set Linear Advance K value</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> none</span
            >
            <span class="label label-requires"><code>TMC2130</code></span>
            <span class="label label-requires"><code>TMC2208</code></span>
            <span class="label label-requires"><code>TMC2660</code></span>
            <h2>
              <a href="/docs/gcode/M906.html">M906 - TMC Motor Current</a>
            </h2>
            <p>Set the motor current (in milliamps)</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code
                >DIGIPOTSS_PIN|HAS_MOTOR_CURRENT_PWM|DIGIPOT_I2C|DAC_STEPPER_CURRENT</code
              ></span
            >
            <h2>
              <a href="/docs/gcode/M907.html">M907 - Set Motor Current</a>
            </h2>
            <p>Set motor current via digital trimpot</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>DAC_STEPPER_CURRENT|DIGIPOTSS_PIN</code></span
            >
            <h2><a href="/docs/gcode/M908.html">M908 - Set Trimpot Pins</a></h2>
            <p>Set a digital trimpot directly</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>DAC_STEPPER_CURRENT</code></span
            >
            <h2><a href="/docs/gcode/M909.html">M909 - DAC Print Values</a></h2>
            <p>Report DAC current values to host</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>DAC_STEPPER_CURRENT</code></span
            >
            <h2>
              <a href="/docs/gcode/M910.html">M910 - Commit DAC to EEPROM</a>
            </h2>
            <p>Commit digipot/DAC value to external EEPROM</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>TMC2130|TMC2208|TMC2209|TMC2660</code></span
            >
            <span class="label label-requires"
              ><code> MONITOR_DRIVER_STATUS</code></span
            >
            <h2>
              <a href="/docs/gcode/M911.html"
                >M911 - TMC OT Pre-Warn Condition</a
              >
            </h2>
            <p>Driver overtemperature pre-warn condition</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>TMC2130|TMC2208|TMC2209|TMC2660</code></span
            >
            <span class="label label-requires"
              ><code> MONITOR_DRIVER_STATUS</code></span
            >
            <h2>
              <a href="/docs/gcode/M912.html">M912 - Clear TMC OT Pre-Warn</a>
            </h2>
            <p>Clear overtemperature pre-warn condition flag</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>TMC2130|TMC2208|TMC2209</code></span
            >
            <span class="label label-requires"
              ><code> HYBRID_THRESHOLD</code></span
            >
            <h2>
              <a href="/docs/gcode/M913.html"
                >M913 - Set Hybrid Threshold Speed</a
              >
            </h2>
            <p>TMC driver switching to spreadCycle</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"
              ><code>SENSORLESS_HOMING</code></span
            >
            <h2>
              <a href="/docs/gcode/M914.html">M914 - TMC Bump Sensitivity</a>
            </h2>
            <p>Set sensorless homing sensitivity</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <span class="label label-requires"><code>TMC2130</code></span>
            <span class="label label-requires"
              ><code>TMC_Z_CALIBRATION</code></span
            >
            <h2>
              <a href="/docs/gcode/M915.html">M915 - TMC Z axis calibration</a>
            </h2>
            <p>Align ends of the Z axis and test torque</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> L6474</span
            >
            <span class="label label-requires"
              ><code>MONITOR_L6470_DRIVER_STATUS</code></span
            >
            <h2>
              <a href="/docs/gcode/M916.html"
                >M916 - L6474 Thermal Warning Test</a
              >
            </h2>
            <p>Find L6474 drive level (KVAL_HOLD) threshold</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> L6474</span
            >
            <span class="label label-requires"
              ><code>MONITOR_L6470_DRIVER_STATUS</code></span
            >
            <h2>
              <a href="/docs/gcode/M917.html"
                >M917 - L6474 Overcurrent Warning Test</a
              >
            </h2>
            <p>Find L6474 minimum current thresholds</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> L6474</span
            >
            <span class="label label-requires"
              ><code>MONITOR_L6470_DRIVER_STATUS</code></span
            >
            <h2>
              <a href="/docs/gcode/M918.html"
                >M918 - L6474 Speed Warning Test</a
              >
            </h2>
            <p>Find L6474 speed threshold</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <h2><a href="/docs/gcode/M928.html">M928 - Start SD Logging</a></h2>
            <p>Log serial input to an SD file</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>MAGNETIC_PARKING_EXTRUDER</code></span
            >
            <h2>
              <a href="/docs/gcode/M951.html"
                >M951 - Magnetic Parking Extruder</a
              >
            </h2>
            <p>Set / report Magnetic Parking Extruder settings</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> sdcard</span
            >
            <span class="label label-requires"><code>HAS_SPI_FLASH</code></span>
            <span class="label label-requires"><code> SDSUPPORT</code></span>
            <span class="label label-requires"
              ><code> MARLIN_DEV_MODE</code></span
            >
            <h2>
              <a href="/docs/gcode/M993.html">M993-M994 - SD / SPI Flash</a>
            </h2>
            <p>load or back up SPI Flash and SD</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> calibration</span
            >
            <span class="label label-requires"
              ><code>TOUCH_SCREEN_CALIBRATION</code></span
            >
            <h2>
              <a href="/docs/gcode/M995.html"
                >M995 - Touch Screen Calibration</a
              >
            </h2>
            <p>Touch screen calibration for TFT display</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-success"
              ><span
                data-toggle="tooltip"
                data-placement="bottom"
                title=""
                data-original-title="Available since"
                ><i class="fa fa-code" aria-hidden="true"></i> 2.0.0</span
              ></span
            >
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <h2><a href="/docs/gcode/M997.html">M997 - Firmware update</a></h2>
            <p>Perform in-application firmware update</p>
          </div>
          <div class="gcode item">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <h2><a href="/docs/gcode/M999.html">M999 - STOP Restart</a></h2>
            <p>Return the machine to Running state</p>
          </div>
          <div class="gcode item odd">
            <span class="label label-default"
              ><i class="fa fa-tags" aria-hidden="true"></i> control</span
            >
            <h2>
              <a href="/docs/gcode/T001-T002.html">T0-T6 - Select Tool</a>
            </h2>
            <p>Switch to the specified tool</p>
          </div>
        </div>
      </v-card-text>
      <!-- <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="green darken-1"
            text
            @click="dialog = false"
          >
            Disagree
          </v-btn>
          <v-btn
            color="green darken-1"
            text
            @click="dialog = false"
          >
            Agree
          </v-btn>
        </v-card-actions> -->
    </v-card>
  </v-row>
</template>

<script>
export default {};
</script>

<style>
.gcode {
  margin: 10px 0;
  border-radius: 8px;
  background-color: #f0f0f0;
  padding: 8px 12px;
}
</style>