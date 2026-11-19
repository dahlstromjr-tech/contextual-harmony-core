export enum UIState {
  DORMANT = "DORMANT",
  AMBIENT = "AMBIENT",
  ACTIVE = "ACTIVE"
}

export interface UserContextSignal {
  attentionImpactScore: number;
  urgencyFlag: boolean;
  userExplicitlyRequested: boolean;
}

export class AmbientUXStateMachine {
  private currentState: UIState = UIState.DORMANT;
  private readonly aisThreshold: number = 0.4;

  public evaluateSignal(signal: UserContextSignal): UIState {
    if (signal.userExplicitlyRequested || signal.urgencyFlag) {
      this.currentState = UIState.ACTIVE;
    } else if (signal.attentionImpactScore < this.aisThreshold) {
      this.currentState = UIState.DORMANT;
    } else if (signal.attentionImpactScore < 0.8) {
      this.currentState = UIState.AMBIENT;
    } else {
      this.currentState = UIState.ACTIVE;
    }

    return this.currentState;
  }
}
