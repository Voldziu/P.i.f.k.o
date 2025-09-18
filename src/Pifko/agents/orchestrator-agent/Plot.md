# Pifko Brewery System - Orchestrator's Guide

## System Architecture Overview

The Pifko Brewery System is a distributed microservices architecture consisting of three core services, each with its own PostgreSQL database:

- **Orders Service** (Port 8001): Manages customer orders, invoices, and order tracking
- **Brewery Service** (Port 8002): Handles beer production, recipes, and local ingredient storage
- **Master Storage Service** (Port 8003): Manages central ingredient inventory and allocation

## Agent System & Responsibilities

### Production Agent
**Primary Responsibilities:**
- Monitor production capacity and fermentation/aging storage availability
- Coordinate ingredient allocation from Master Storage to Brewery local storage
- Track brewing schedules and production timelines
- Manage fermentation and aging process monitoring
- Alert when storage capacity limits are reached

**Key Actions:**
- `check_production_capacity(beer_id, quantity)`
- `request_ingredients(recipe_id, batch_size)`
- `start_fermentation_batch(beer_id, quantity)`
- `monitor_aging_progress(batch_id)`
- `release_storage_capacity(batch_id)`

### Inventory Agent
**Primary Responsibilities:**
- Monitor ingredient levels across local brewery storage
- Trigger restocking alerts when minimum levels are reached

**Key Actions:**
- `check_ingredient_availability(ingredient_type, ingredient_id, quantity_needed)`
- `allocate_ingredients(allocation_request)`

### Order Agent
**Primary Responsibilities:**
- Process incoming customer orders
- Process order status queries
- Ask orders-db for given order content
- Only him can manage Order statuses
- Handle order modifications and cancellations


**Key Actions:**
- `check_beer_availability(beer_id, quantity)`
- `update_order_status(order_id, new_status)`


## Beer Making Process

### 1. Ingredients Gathering Phase
**Objective:** Ensure all recipe ingredients are available in sufficient quantities

**Process Flow:**
1. **Recipe Analysis**: Parse recipe requirements (RecipeHopsAssociative, RecipeMaltsAssociative, RecipeYeastAssociative)
2. **Local Storage Check**: Verify brewery's local ingredient storage (LocalHopsStorage, LocalMaltsStorage, LocalYeastsStorage)
3. **Master Storage Request**: Request additional ingredients from Master Storage if local supplies insufficient
4. **Allocation Confirmation**: Confirm all ingredients allocated before proceeding to production

**Key Models Involved:**
- `Recipe` (fermentation_time, aging_time)
- `RecipeHopsAssociative`, `RecipeMaltsAssociative`, `RecipeYeastAssociative`
- `LocalHopsStorage`, `LocalMaltsStorage`, `LocalYeastsStorage`
- `HopsStorage`, `MaltsStorage`, `YeastsStorage` (Master Storage)

### 2. Fermentation Process
**Objective:** Transform ingredients into beer through controlled fermentation

**Process Requirements:**
- **Storage Capacity Check**: Verify fermentation tanks available
- **Duration Tracking**: Monitor fermentation time from Recipe.fermentation_time
- **Resource Consumption**: Deduct ingredients from local storage
- **Capacity Management**: Reserve fermentation space for specified duration

**Critical Constraints:**
- Maximum fermentation storage capacity must be tracked
- Cannot start new fermentation without available fermentation space
- Fermentation time varies by beer type (14-28 days typical)

### 3. Aging Process
**Objective:** Mature beer to achieve desired flavor profile

**Process Requirements:**
- **Aging Storage Check**: Verify aging storage availability after fermentation
- **Duration Tracking**: Monitor aging time from Recipe.aging_time  
- **Storage Transfer**: Move from fermentation to aging storage
- **Capacity Planning**: Ensure aging storage available for full aging period

**Critical Constraints:**
- Maximum aging storage capacity must be tracked
- Aging times vary significantly (30-90 days typical)
- Cannot complete fermentation without confirmed aging space
- Must plan aging storage weeks in advance due to long durations



### Order Status Management

### Two-Level Status System

The system uses **dual-level status tracking**:
- **OrderStatus**: High-level customer-facing order lifecycle
- **OrderStatusInner**: Detailed production stage tracking (active only during IN_PRODUCTION)

### Primary Order Status Flow
```
PENDING → CONFIRMED → IN_PRODUCTION → DONE
    ↓         ↓            ↓         ↓
CANCELLED  CANCELLED   CANCELLED  CANCELLED
```

### Production Detail Status Flow (OrderStatusInner)
```
When OrderStatus = IN_PRODUCTION:

PENDING  → READY_FOR_PRODUCTION → READY_FOR_FERMENTING → 
FERMENTING → DONE_FERMENTING → READY_FOR_AGING → AGING → DONE_AGING → DONE
```

## Primary Status Definitions & Actions

#### PENDING
**Definition**: Order received but not yet validated for production capacity
**OrderStatusInner**: N/A (not applicable at this stage). Should be PENDING

**Allowed Actions:**
- `check_ingredients()`: Check ingredient availability
- `check_production_ability()`: Check production ability
- `cancel_order()`: Cancel before production commitment
- `confirm_order()`: Move to READY_FOR_PRODUCTION status

**Restrictions:**
- No production resources reserved
- No ingredients allocated
- Full modification allowed

#### READY_FOR_PRODUCTION  
**Definition**: Order validated and production capacity confirmed
**OrderStatusInner**: N/A (not applicable at this stage). Should be PENDING

**Allowed Actions:**
- `cancel_order()`: Cancel with potential restocking fee
- `start_production()`:  Move to IN_PRODUCTION status

**Restrictions:**
- Production slot reserved
- Limited modifications allowed

#### IN_PRODUCTION
**Definition**: Brewing process actively underway
**OrderStatusInner**: Detailed production stage tracking (see Production Detail Statuses below)

**Allowed Actions:**
- `track_production_progress()`: Monitor detailed OrderStatusInner progression

**Restrictions:**
- No order modifications allowed
- Actions depend on current OrderStatusInner stage

#### DONE
**Definition**: Order successfully completed and ready for delivery/pickup
**OrderStatusInner**: DONE (production completed)

**Allowed Actions:**
- `generate_completion_report()`: Final order documentation

**Restrictions:**
- Order immutable - production completed
- Focus on fulfillment and documentation

#### CANCELLED
**Definition**: Order terminated at any stage
**OrderStatusInner**: Preserves last production stage before cancellation

**Allowed Actions:**


## Production Detail Status Definitions (OrderStatusInner)

*Active only when OrderStatus = IN_PRODUCTION*

#### PENDING
**Definition**: Production queued but not yet started

#### READY_TO_PRODUCTION
**Definition**: All ingredients allocated and available, awaiting production start


#### READY_FOR_FERMENTING
**Definition**: Ingredients prepared and ready for fermentation process
**Required Action**: Start fermentation, consume ingredients


#### FERMENTING
**Definition**: Active fermentation process underway
**Duration**: Based on Recipe.fermentation_time

#### DONE_FERMENTING
**Definition**: Fermentation completed, ready for aging transition
**Required Action**: Transfer to aging storage

#### READY_FOR_AGING  
**Definition**: Beer ready for aging process, awaiting aging tank availability


#### AGING
**Definition**: Active aging process underway
**Duration**: Based on Recipe.aging_time  

#### DONE
**Definition**: Production fully completed
**Triggers**: OrderStatus automatically moves to DONE


### Status Transition Rules

**Primary Status Transitions:**
- PENDING → CONFIRMED: When validation passes
- CONFIRMED → IN_PRODUCTION: When production starts (OrderStatusInner = PENDING)
- IN_PRODUCTION → DONE: When OrderStatusInner reaches DONE
- Any status → CANCELLED: Manual intervention

**Production Detail Transitions (OrderStatusInner):**
- PENDING → READY_FOR_PRODUCTION: When all ingredients confirmed available
- READY_FOR_PRODUCTION → READY_FOR_FERMENTING: When production batch prepared
- READY_FOR_FERMENTING → FERMENTING: When fermentation starts. Consumes ingredients.
- FERMENTING → DONE_FERMENTING: After Recipe.fermentation_time elapsed. Possible Manual user activtion.
- DONE_FERMENTING → READY_FOR_AGING: When aging tanks available
- READY_FOR_AGING → AGING: When aging process starts. Possible Manual user activtion.
- AGING → DONE_AGING: After Recipe.aging_time elapsed
- DONE_AGING → DONE: Automatic completion

**Emergency Transitions:**
- Any OrderStatusInner → CANCELLED: Emergency production halt

### Critical Order Management Constraints

1. **Dual-Level Tracking**: OrderStatus provides customer visibility, OrderStatusInner enables operational control
2. **Stage-Based Cancellation**: Costs increase progressively through OrderStatusInner stages
3. **Capacity Management**: FERMENTING and AGING stages must respect storage capacity limits
4. **Timeline Validation**: Must account for full fermentation + aging duration in delivery estimates
5. **Resource Cascade**: Status changes trigger appropriate resource allocation/release actions