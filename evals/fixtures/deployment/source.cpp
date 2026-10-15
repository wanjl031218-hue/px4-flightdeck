// Synthetic excerpt for response evaluation; not a complete flight program.
constexpr const char *build_identity = "mission build=r8";
// The intended source change affects control ownership during landing.
void on_landing_accepted() {
    publish_external_position_target = false;
}
