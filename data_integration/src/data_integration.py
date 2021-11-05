import pandas as pd
import numpy as np
import time
import collections


def df_set(df_trr, df_weapondischarge, df_trrstatus, sub_weapon_refresh):
    """Set necessary df."""
    # Set trr_trr_refresh
    df_trr["trr_datetime"] = pd.to_datetime(df_trr["trr_datetime"])
    df_trr["beat"] = df_trr["beat"].astype(int)
    df_trr["officer_appointed_date"] = pd.to_datetime(
        reformat_date(df_trr["officer_appointed_date"])
    ).strftime("%Y-%m-%d")
    df_trr["officer_birth_year"] = df_trr["officer_birth_year"].fillna(0.0).astype(int)
    df_trr["officer_birth_year"].replace(0, np.nan, inplace=True)
    df_trr["officer_age"] = df_trr["officer_age"].astype(int)
    df_trr["officer_on_duty"] = df_trr["officer_on_duty"].astype(bool)
    df_trr["officer_injured"] = df_trr["officer_injured"].astype(bool)
    df_trr["officer_in_uniform"] = df_trr["officer_in_uniform"].astype(bool)
    df_trr["subject_birth_year"] = df_trr["subject_birth_year"].astype(int)
    df_trr["subject_age"] = df_trr["subject_age"].astype(int)
    df_trr["subject_armed"] = df_trr["subject_armed"].astype(bool)
    df_trr["subject_injured"] = df_trr["subject_injured"].astype(bool)
    df_trr["subject_alleged_injury"] = df_trr["subject_alleged_injury"].astype(bool)
    df_trr["notify_oemc"] = df_trr["notify_oemc"].astype(bool)
    df_trr["notify_district_sergeant"] = df_trr["notify_district_sergeant"].astype(bool)
    df_trr["notify_op_command"] = df_trr["notify_op_command"].astype(bool)
    df_trr["notify_det_division"] = df_trr["notify_det_division"].astype(bool)
    df_trr["trr_created"] = pd.to_datetime(df_trr["trr_created"])

    # Set trr_weapondischarge_refresh
    df_weapondischarge["firearm_reloaded"] = df_weapondischarge[
        "firearm_reloaded"
    ].astype(bool)
    df_weapondischarge["sight_used"] = df_weapondischarge["sight_used"].astype(bool)

    # Set trr_trrstatus_refresh
    df_trrstatus["officer_appointed_date"] = pd.to_datetime(
        reformat_date(df_trrstatus["officer_appointed_date"])
    ).strftime("%Y-%m-%d")
    df_trrstatus["officer_birth_year"] = (
        df_trrstatus["officer_birth_year"].fillna(0).astype(int)
    )
    df_trrstatus["officer_birth_year"].replace(0, np.nan, inplace=True)
    df_trrstatus["status_datetime"] = pd.to_datetime(df_trrstatus["status_datetime"])

    # Set trr_subjectweapon_refresh
    # Weapon, change specific items to the correct form.
    sub_weapon_refresh.loc[
        (sub_weapon_refresh.weapon_type == "CHEMICAL WEAPON")
        | (sub_weapon_refresh.weapon_type == "TASER / STUN GUN"),
        "weapon_type",
    ] = "OTHER (SPECIFY)"
    sub_weapon_refresh.loc[
        (sub_weapon_refresh.weapon_type == "VEHICLE"), "weapon_type"
    ] = "VEHICLE - ATTEMPTED TO STRIKE OFFICER WITH VEHICLE"

    # Change location format
    # Indoor/outdoor change specific column.
    df_trr.loc[(df_trr.indoor_or_outdoor == "OUTDOOR"), "indoor_or_outdoor"] = "Outdoor"
    df_trr.loc[(df_trr.indoor_or_outdoor == "INDOOR"), "indoor_or_outdoor"] = "Indoor"

    # Street. 1. change to camel case
    df_trr["street"] = df_trr["street"].str.title()

    # location. 1. change to camel case 2. change specific items to the correct form.
    df_trr["location"] = df_trr["location"].str.title()

    df_trr.loc[
        (df_trr.location == "Cha Hallway / Stairwell / Elevator"), "location"
    ] = "Cha Hallway/Stairwell/Elevator"
    df_trr.loc[
        (df_trr.location == "Cha Parking Lot / Grounds"), "location"
    ] = "Cha Parking Lot/Grounds"
    df_trr.loc[
        (df_trr.location == "Church / Synagogue / Place Of Worship"), "location"
    ] = "Church/Synagogue/Place Of Worship"
    df_trr.loc[
        (df_trr.location == "College / University - Grounds"), "location"
    ] = "College/University Grounds"
    df_trr.loc[
        (df_trr.location == "Factory / Manufacturing Building"), "location"
    ] = "Factory/Manufacturing Building"
    df_trr.loc[
        (df_trr.location == "Government Building / Property"), "location"
    ] = "Government Building/Property"
    df_trr.loc[
        (df_trr.location == "Highway / Expressway"), "location"
    ] = "Highway/Expressway"
    df_trr.loc[
        (df_trr.location == "Hospital Building / Grounds"), "location"
    ] = "Hospital Building/Grounds"
    df_trr.loc[(df_trr.location == "Hotel / Motel"), "location"] = "Hotel/Motel"
    df_trr.loc[
        (df_trr.location == "Movie House / Theater"), "location"
    ] = "Movie House/Theater"
    df_trr.loc[
        (df_trr.location == "Nursing / Retirement Home"), "location"
    ] = "Nursing Home/Retirement Home"
    df_trr.loc[(df_trr.location == "Other (Specify)"), "location"] = "Other"
    df_trr.loc[
        (df_trr.location == "Other Railroad Property / Train Depot"), "location"
    ] = "Other Railroad Prop / Train Depot"
    df_trr.loc[
        (df_trr.location == "Parking Lot / Garage (Non Residential)"), "location"
    ] = "Parking Lot/Garage(Non.Resid.)"
    df_trr.loc[
        (df_trr.location == "Other Railroad Property / Train Depot"), "location"
    ] = "Other Railroad Prop / Train Depot"
    df_trr.loc[
        (df_trr.location == "Police Facility / Vehicle Parking Lot"), "location"
    ] = "Police Facility/Veh Parking Lot"
    df_trr.loc[
        (df_trr.location == "Residence - Porch / Hallway"), "location"
    ] = "Residence Porch/Hallway"
    df_trr.loc[
        (df_trr.location == "Residence - Garage"), "location"
    ] = "Residence-Garage"
    df_trr.loc[
        (df_trr.location == "Residence - Yard (Front / Back)"), "location"
    ] = "Residential Yard (Front/Back)"
    df_trr.loc[
        (df_trr.location == "School - Private Building"), "location"
    ] = "School, Private, Building"
    df_trr.loc[
        (df_trr.location == "School - Private Grounds"), "location"
    ] = "School, Private, Grounds"
    df_trr.loc[
        (df_trr.location == "School - Public Building"), "location"
    ] = "School, Public, Building"
    df_trr.loc[
        (df_trr.location == "School - Public Grounds"), "location"
    ] = "School, Public, Grounds"
    df_trr.loc[
        (df_trr.location == "Sports Arena / Stadium"), "location"
    ] = "Sports Arena/Stadium"
    df_trr.loc[
        (df_trr.location == "Tavern / Liquor Store"), "location"
    ] = "Tavern/Liquor Store"
    df_trr.loc[(df_trr.location == "Vacant Lot / Land"), "location"] = "Vacant Lot/Land"
    df_trr.loc[
        (df_trr.location == "Vehicle - Other Ride Share Service (Lyft, Uber, Etc.)"),
        "location",
    ] = "Vehicle - Other Ride Service"
    df_trr.loc[
        (df_trr.location == "Vehicle - Commercial"), "location"
    ] = "Vehicle-Commercial"
    df_trr.loc[
        (df_trr.location == "Cta Parking Lot / Garage / Other Property"), "location"
    ] = "Cta Garage / Other Property"
    df_trr.loc[
        (df_trr.location == "Lakefront / Waterfront / Riverbank"), "location"
    ] = "Lakefront/Waterfront/Riverbank"
    df_trr.loc[
        (df_trr.location == "Medical / Dental Office"), "location"
    ] = "Medical/Dental Office"
    df_trr.loc[
        (df_trr.location == "Airport Parking Lot"), "location"
    ] = "Airport/Aircraft"
    df_trr.loc[
        (df_trr.location == "Airport Terminal Mezzanine - Non-Secure Area"), "location"
    ] = "Airport Terminal Lower Level - Non-Secure Area"


def reformat_date(df):
    """REDACTED => NAN, DD-MM-YY =>YYYY=MM-DD, DD-MON-YY => YYYY-MM-DD"""
    appoint_date = []
    for i in range(len(df)):
        day = df[i]
        if pd.isna(day):
            appoint_date.append(np.nan)
        elif day == "REDACTED":
            appoint_date.append(np.nan)
        elif len(day) == 8:
            if int(day[6:8]) + 2000 > 2021:
                appoint_date.append("19" + day[6:8] + "-" + day[0:5])
            else:
                appoint_date.append("20" + day[6:8] + "-" + day[0:5])
        else:
            mon = day[5:8]
            if mon == "JAN":
                appoint_date.append(day[0:5] + "01" + day[8:])
            elif mon == "FEB":
                appoint_date.append(day[0:5] + "02" + day[8:])
            elif mon == "MAR":
                appoint_date.append(day[0:5] + "03" + day[8:])
            elif mon == "APR":
                appoint_date.append(day[0:5] + "04" + day[8:])
            elif mon == "MAY":
                appoint_date.append(day[0:5] + "05" + day[8:])
            elif mon == "JUN":
                appoint_date.append(day[0:5] + "06" + day[8:])
            elif mon == "JUL":
                appoint_date.append(day[0:5] + "07" + day[8:])
            elif mon == "AUG":
                appoint_date.append(day[0:5] + "08" + day[8:])
            elif mon == "SEP":
                appoint_date.append(day[0:5] + "09" + day[8:])
            elif mon == "OCT":
                appoint_date.append(day[0:5] + "10" + day[8:])
            elif mon == "NOV":
                appoint_date.append(day[0:5] + "11" + day[8:])
            elif mon == "DEC":
                appoint_date.append(day[0:5] + "12" + day[8:])
    return appoint_date


def reconciliation_race(df):
    """Replace the format as race_map shows."""
    race_map = dict(
        {
            "AMER IND/ALASKAN NATIVE": "NATIVE AMERICAN/ALASKAN NATIVE",
            "AMER INDIAN / ALASKAN NATIVE": "NATIVE AMERICAN/ALASKAN NATIVE",
            "ASIAN / PACIFIC ISLANDER": "ASIAN/PACIFIC ISLANDER",
            "ASIAN/PACIFIC ISLANDER": "ASIAN/PACIFIC ISLANDER",
            "BLACK": "BLACK",
            "UNKNOWN": "NULL",
            "UNKNOWN / REFUSED": "NULL",
            "HISPANIC": "HISPANIC",
            "WHITE": "WHITE",
        }
    )
    for k in race_map:
        if k[0:2] == "UN":
            df.replace(k, np.nan, inplace=True)
        else:
            df.replace(k, race_map[k], inplace=True)


def reconciliation_gender(df):
    race_map = dict({"FEMALE": "F", "MALE": "M"})
    for k in race_map:
        df.replace(k, race_map[k], inplace=True)


def reconciliation_birth_year(df):
    birth_years = df.to_numpy()
    birth_years[birth_years < 100] += 1900
    birth_years[birth_years < 200] *= 10
    for i in range(1000, 2000, 100):
        birth_years[birth_years < i] += 2000 - i
    df = pd.DataFrame(birth_years)


def age_sanity(row):
    if row < 100:
        return 1900 + row
    if 100 <= row < 1900:
        return 1900 + row % 100
    return row


def update_last_suffix(df):
    df["suffix_name"] = "NULL"

    suffix_list = ["I", "II", "III", "IV", "V", "JR", "SR"]
    officer_last_name = []
    suffix_name = []
    for i in df["officer_last_name"]:
        target_str = i.upper().split(" ")
        if len(target_str) > 1:
            k = 0
            for j in suffix_list:
                if j == "".join(e for e in target_str[-1] if e.isalnum()):
                    # print(''.join(e for e in target_str[-1] if e.isalnum()))
                    suffix_name.append(j)
                    k += 1
            if k == 0:
                suffix_name.append(None)
            officer_last_name.append(" ".join(target_str).title())
        else:
            officer_last_name.append(i.title())
            suffix_name.append(None)
    df["officer_last_name"] = officer_last_name
    df["suffix_name"] = suffix_name


def update_first_name(df):
    officer_first_name = []
    for i in df["officer_first_name"]:
        officer_first_name.append(i.title())
    df["officer_first_name"] = officer_first_name


def update_race(df):
    race_map = dict(
        {
            "AMER IND/ALASKAN NATIVE": "Native American/Alaskan Native",
            "ASIAN/PACIFIC ISLANDER": "Asian/Pacific",
            "BLACK": "Black",
            "UNKNOWN": "Unknown",
            "HISPANIC": "Hispanic",
            "WHITE": "White",
            "WHITE HISPANIC": "Hispanic",
            "BLACK HISPANIC": "Hispanic",
        }
    )
    for k in race_map:
        df.replace(k, race_map[k], inplace=True)


def add_officer_id(df, df_officer):
    df["officer_id"] = "NULL"

    fields = [
        "first_name",
        "middle_initial",
        "last_name",
        "suffix_name",
        "birth_year",
        "appointed_date",
        "gender",
        "race",
    ]
    officer_fields = [
        "officer_first_name",
        "officer_middle_initial",
        "officer_last_name",
        "suffix_name",
        "officer_birth_year",
        "officer_appointed_date",
        "officer_gender",
        "officer_race",
    ]

    officer_id = []
    index = []
    for i, officer in df.iterrows():
        count = np.zeros(len(df_officer))
        for j in range(8):
            count += (
                pd.isna(df_officer[fields[j]]) | pd.isna(officer[officer_fields[j]])
            ).to_numpy() * 0.9
            count += (df_officer[fields[j]] == officer[officer_fields[j]]).to_numpy()
        index.append(np.argmax(count))
        officer_id.append(df_officer.loc[index[i]]["id"])
    df["officer_id"] = officer_id


def re_order(
    df_trr,
    df_unit,
    df_actionresponse,
    df_weapondischarge,
    df_trrstatus,
    sub_weapon_refresh,
):
    df_trr["unit_name_padded"] = df_trr.officer_unit_name.apply(lambda x: x.zfill(3))
    df_trr_new = pd.merge(
        df_trr, df_unit, how="left", left_on="unit_name_padded", right_on="unit_name"
    )
    df_trr_new.rename(
        {"id_y": "officer_unit_id", "description": "officer_unit_detail_id"},
        axis=1,
        inplace=True,
    )
    df_trr_new.drop(
        [
            "unit_name_padded",
            "tags",
            "active",
            "created_at",
            "updated_at",
            "unit_name",
            "officer_unit_name",
        ],
        axis=1,
        inplace=True,
    )
    # Instructed order.
    trr_output_order = "id, crid, event_id, beat, block, direction, street, location, trr_datetime, indoor_or_outdoor, lighting_condition, weather_condition, notify_OEMC, notify_district_sergeant, notify_OP_command, notify_DET_division, party_fired_first, officer_assigned_beat, officer_on_duty, officer_in_uniform, officer_injured, officer_rank, subject_armed, subject_injured, subject_alleged_injury, subject_age, subject_birth_year, subject_gender, subject_race, officer_id, officer_unit_id, officer_unit_detail_id, point"
    trr_actionresponse_output_order = (
        "person, resistance_type, action, other_description, trr_id"
    )
    trr_weapondischarge_output_order = "weapon_type,weapon_type_description,firearm_make,firearm_model,firearm_barrel_length,firearm_caliber,total_number_of_shots,firearm_reloaded,number_of_cartridge_reloaded,handgun_worn_type,handgun_drawn_type,method_used_to_reload,sight_used,protective_cover_used,discharge_distance,object_struck_of_discharge,discharge_position,trr_id"
    trr_trrstatus_output_order = (
        "rank, star, status, status_datetime, officer_id, trr_id"
    )
    trr_subjectweapon_output_order = (
        "weapon_type, firearm_caliber, weapon_description, trr_id"
    )

    # Rename columns.
    df_trr_new.rename(
        {
            "id_x": "id",
            "event_number": "event_id",
            "cr_number": "crid",
            "notify_oemc": "notify_OEMC",
            "notify_op_command": "notify_OP_command",
            "notify_det_division": "notify_DET_division",
        },
        axis=1,
        inplace=True,
    )
    df_actionresponse.rename({"trr_report_id": "trr_id"}, axis=1, inplace=True)
    df_weapondischarge.rename({"trr_report_id": "trr_id"}, axis=1, inplace=True)
    df_trrstatus.rename(
        {"officer_rank": "rank", "officer_star": "star", "trr_report_id": "trr_id"},
        axis=1,
        inplace=True,
    )
    sub_weapon_refresh.rename({"trr_report_id": "trr_id"}, axis=1, inplace=True)

    # Reorder columns
    df_trr = df_trr_new[trr_output_order.replace(" ", "").split(",")]
    df_trrstatus = df_trrstatus[trr_trrstatus_output_order.replace(" ", "").split(",")]
    return df_trr,df_trrstatus

def check_key(
    df_trr,
    df_weapondischarge,
    df_trrstatus,
    df_actionresponse,
    df_charge,
    sub_weapon_refresh,
):
    """Check if there are unmatched item in supporting tables."""
    # Get unique id of each table key
    # Primary key
    ancher = set(df_trr.id.unique())
    # Foreign Key
    weapondischarge_set = set(df_weapondischarge.trr_report_id.unique())
    trrstatus_set = set(df_trrstatus.trr_report_id.unique())
    actionresponse_set = set(df_actionresponse.trr_report_id.unique())
    charge_set = set(df_charge.trr_report_id.unique())
    sub_weapon_refresh_set = set(sub_weapon_refresh.trr_report_id.unique())

    # Discard unused keys
    discard_item(
        ancher, weapondischarge_set, df_weapondischarge,
    )
    discard_item(
        ancher, trrstatus_set, df_trrstatus,
    )
    discard_item(
        ancher, actionresponse_set, df_actionresponse,
    )
    discard_item(
        ancher, charge_set, df_charge,
    )
    discard_item(
        ancher, sub_weapon_refresh_set, sub_weapon_refresh,
    )


def discard_item(ancher, helper, df_name):
    unused = helper - ancher
    if len(unused):
        print("Has unused.")
        print(unused)
    else:
        print("All good.")
    for key in unused:
        df_name = df_name[df_name.trr_report_id != key]


def main():
    print("Loading Data...")
    # Import trr_trr_refresh
    df_trr = pd.read_csv("data/trr_trr_refresh.csv")
    # Import trr_weapondischarge_refresh
    df_weapondischarge = pd.read_csv("data/trr_weapondischarge_refresh.csv")
    # Import trr_trrstatus_refresh
    df_trrstatus = pd.read_csv("data/trr_trrstatus_refresh.csv")
    # Import trr_subjectweapon_refresh
    sub_weapon_refresh = pd.read_csv("data/trr_subjectweapon_refresh.csv")
    # Import trr_charge_refresh
    df_charge = pd.read_csv("data/trr_charge_refresh.csv")
    # Import trr_actionresponse_refresh
    df_actionresponse = pd.read_csv("data/trr_actionresponse_refresh.csv")
    # Import data_officer
    df_officer = pd.read_csv("data/data_officer.csv")
    # Import data_policeunit
    df_unit = pd.read_csv("data/data_policeunit.csv", dtype=str)
    print("Loading Finished")
    print("--------------------")
    # Set df
    print("Processing Type Correction...")
    df_set(df_trr, df_weapondischarge, df_trrstatus, sub_weapon_refresh)
    print("Type Correction Done")
    print("--------------------")
    print("Processing Reconciliation...")
    reconciliation_race(df_trr["subject_race"])
    reconciliation_gender(df_trr["subject_gender"])
    reconciliation_birth_year(df_trrstatus["officer_birth_year"])
    reconciliation_birth_year(df_trr["subject_birth_year"])
    df_trr.subject_birth_year = df_trr.subject_birth_year.apply(age_sanity)
    update_last_suffix(df_trrstatus)
    update_last_suffix(df_trr)
    update_first_name(df_trrstatus)
    update_first_name(df_trr)
    update_race(df_trrstatus)
    update_race(df_trr)
    print("Reconciliation Done")
    print("--------------------")
    print("Processing Linking the Officers with trr_trr_refresh...")
    print("It may take 5 minutes.")
    add_officer_id(df_trr, df_officer)
    print("Linking the Officers with trr_trr_refresh Finished")
    print("--------------------")
    print("Processing Linking the Officers with trr_trr_refresh...")
    print("It may take 20 minutes.")
    add_officer_id(df_trrstatus, df_officer)
    print("Linking the Officers with trr_trr_refresh Finished")
    print("--------------------")
    print("Processing Linking the Police Unit IDs...")
    #
    # merge rank and star
    #
    df_trr = df_trr.drop(
        columns=[
            "officer_first_name",
            "officer_middle_initial",
            "officer_last_name",
            "suffix_name",
            "officer_birth_year",
            "officer_appointed_date",
            "officer_gender",
            "officer_race",
        ]
    )
    df_trrstatus = df_trrstatus.drop(
        columns=[
            "officer_first_name",
            "officer_middle_initial",
            "officer_last_name",
            "suffix_name",
            "officer_birth_year",
            "officer_appointed_date",
            "officer_gender",
            "officer_race",
        ]
    )
    check_key(
        df_trr,
        df_weapondischarge,
        df_trrstatus,
        df_actionresponse,
        df_charge,
        sub_weapon_refresh,
    )

    df_trr, df_trrstatus = re_order(
        df_trr,
        df_unit,
        df_actionresponse,
        df_weapondischarge,
        df_trrstatus,
        sub_weapon_refresh,
    )
    print("--------------------")
    print("Processing Output...")
    df_trr.to_csv(r"../output/trr-trr.csv", index=False)
    df_weapondischarge.to_csv(r"../output/trr-weapondischarge.csv", index=False)
    df_trrstatus.to_csv(r"../output/trr-trrstatus.csv", index=False)
    sub_weapon_refresh.to_csv(r"../output/trr-subjectweapon.csv", index=False)
    df_charge.to_csv(r"../output/trr-charge.csv", index=False)
    df_actionresponse.to_csv(r"../output/trr-actionresponse.csv", index=False)
    print("Everything is Done")


if __name__ == "__main__":
    main()
